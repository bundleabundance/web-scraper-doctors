import django_filters
from .models import Doctor,Review,Cv, Appointment

class DoctorFilter(django_filters.FilterSet):
    class Meta:
        model = Doctor
        fields = {
            'name': ['exact', 'icontains'],
            'specialty': ['exact', 'icontains'],
            'institution': ['exact'],
            'experience': ['exact', 'gt', 'lt'],
            'accepted_insurance_providers': ['exact'],
        }
class ReviewFilter(django_filters.FilterSet):
    class Meta:
        model = Review
        fields = {
            'doctor': ['exact'],
            'patient': ['exact'],
            'rating': ['exact', 'gt', 'lt'],
        }
class CvFilter(django_filters.FilterSet):
   class Meta:
       model = Cv
       fields = {
            'doctor': ['exact'],
             }
       
class AppointmentFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = {
            'patient': ['exact'],
            'doctor': ['exact'],
            'time_slot': ['exact', 'icontains'],
            'status': ['exact'],
            'date': ['exact', 'gt', 'lt'],
        }
        