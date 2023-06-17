"""
URL configuration for doctor_scraper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DoctorViewSet, InstitutionViewSet, InsuranceViewSet, PatientViewSet, HealthRecordViewSet, AppointmentViewSet, ReviewViewSet,my_view,doctor,doctor2,doctor3,doctor_review,doctor_personalpage,media_view,scrape_doctors_endpoint,CvViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('doctors', DoctorViewSet, basename='doctor')
router.register('institutions', InstitutionViewSet, basename='institution')
router.register('insurances', InsuranceViewSet, basename='insurance')
router.register('patients', PatientViewSet, basename='patient') 
router.register('health_records', HealthRecordViewSet, basename='healthrecord')
router.register('appointments', AppointmentViewSet, basename='appointment')
router.register('reviews', ReviewViewSet, basename='review')
router.register('cv', CvViewSet, basename='cv')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('my-url/', my_view, name='my_view'),
    path('doctor/', doctor, name='doctor'),
        path('doctor2/', doctor2, name='doctor'),
        path('doctor3/', doctor3, name='doctor'),
        path('doctor_review/', doctor_review, name='doctor'),
    path('doctor_personalpage/', doctor_personalpage, name='doctor'),
        path('media/<path:file_path>', media_view, name='media'),
            path('scrape-doctors/', scrape_doctors_endpoint, name='scrape_doctors_endpoint'),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
