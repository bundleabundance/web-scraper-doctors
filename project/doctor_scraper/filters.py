import django_filters
from .models import Doctor,Review,Cv

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