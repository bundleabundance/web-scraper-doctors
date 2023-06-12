from rest_framework import serializers
from .models import CustomUser, Doctor, Institution, Insurance, Patient, HealthRecord, Appointment, Review,Cv

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'role']


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
class CvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cv
        fields = '__all__'
class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
class DoctorSerializer(serializers.ModelSerializer):
    accepted_insurance_providers = InsuranceSerializer(many=True, read_only=True)
    institution = InstitutionSerializer( read_only=True)
    cv = CvSerializer( read_only=True)
    class Meta:
        model = Doctor
        fields = ['id','name', 'specialty', 'institution', 'experience', 'photo', 'phone', 'rating', 'accepted_insurance_providers','cv']

