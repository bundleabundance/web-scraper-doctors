from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin')
    ]
    role = models.CharField(choices=ROLE_CHOICES, default='patient', max_length=10)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',  # Add a unique related_name
        related_query_name='customuser'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',  # Add a unique related_name
        related_query_name='customuser'
    )


class Institution(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    services_offered = models.TextField()


class Insurance(models.Model):
    name = models.CharField(max_length=255)
    coverage_details = models.TextField()
class Services(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class Cv(models.Model):
    languages = models.TextField()
    interests = models.TextField()
    educations = models.TextField()
    about = models.TextField()

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    experience = models.IntegerField(default=0)
    accepted_insurance_providers = models.ManyToManyField(Insurance)
    cv= models.ForeignKey(Cv, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.CharField(max_length=600, null=True, blank=True)
    services = models.ManyToManyField(Services) # Here is the ManyToManyField
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    sub_specialty = models.CharField(max_length=255, null=True, blank=True)
    @property
    def rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg']



class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)


class HealthRecord(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    allergies = models.TextField()
    past_surgeries = models.TextField()
    ongoing_treatments = models.TextField()
    family_history = models.TextField()


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time_slot = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, default='scheduled', max_length=10)
    date = models.DateField()

class Review(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review_text = models.TextField()
    date = models.DateField()