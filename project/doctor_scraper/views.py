from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from bs4 import BeautifulSoup
from .models import CustomUser, Doctor, Institution, Insurance, Patient, HealthRecord, Appointment, Review,Services,Cv
from .serializers import UserSerializer, DoctorSerializer, InstitutionSerializer, InsuranceSerializer, PatientSerializer, HealthRecordSerializer, AppointmentSerializer, ReviewSerializer,CvSerializer
from django.shortcuts import render
from .filters import DoctorFilter,ReviewFilter,CvFilter, AppointmentFilter
from django.conf import settings
from django.http import HttpResponseNotFound, FileResponse
import os
import requests
import re
from django.http import HttpResponse, JsonResponse

from urllib.parse import urlparse, parse_qs

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DoctorFilter

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer

class InsuranceViewSet(viewsets.ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class HealthRecordViewSet(viewsets.ModelViewSet):
    queryset = HealthRecord.objects.all()
    serializer_class = HealthRecordSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AppointmentFilter

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
class CvViewSet(viewsets.ModelViewSet):
    queryset = Cv.objects.all()
    serializer_class = CvSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CvFilter
def media_view(request, file_path):
    # Construct the absolute path to the media file
    absolute_path = os.path.join(settings.MEDIA_ROOT, file_path)
    # if request its not empty send request to that url in the request


    # Check if the file exists
    if os.path.exists(absolute_path):
        # Return the file as the response
        return FileResponse(open(absolute_path, 'rb'))

    # If the file doesn't exist, return a 404 response
    return HttpResponseNotFound('File not found')

def index(request):
    return render(request, 'index.html')

def my_view(request):
    return render(request, 'my_template.html')

def doctor(request):
    return render(request, 'doctor.html')

def doctor2(request):
    return render(request, 'doctor2.html')

def doctor3(request):
    return render(request, 'doctor3.html')
def doctor_review(request):
    return render(request, 'doctor_review.html')

def doctor_personalpage(request):
    return render(request, 'doctor_personalpage.html')

def doctor_personalpage2(request):
    return render(request, 'doctor_personalpage2.html')

def book_appointment(request):
    return render(request, 'book_appointment.html')

BASE_URL = 'https://www.doktortakvimi.com/'

def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def scrape_cv(html):
    soup = BeautifulSoup(html, 'html.parser')

    cv_data = {}

    about_me_section = soup.find("div", {"data-test-id": "doctor-exp-about"})
    about_me_text = about_me_section.find('p').text.strip() if about_me_section else ''
    cv_data["about"] = about_me_text

    interest_section = soup.find("div", {"data-test-id": "doctor-exp-disease"})
    interests = [li.text.strip() for li in interest_section.find_all('li')] if interest_section else []
    cv_data["interests"] = interests

    education_section = soup.find("div", {"data-test-id": "doctor-exp-school"})
    educations = [li.text.strip() for li in education_section.find_all('li')] if education_section else []
    cv_data["educations"] = educations


    language_section = soup.find("div", {"data-test-id": "doctor-exp-language"})
    languages = [li.text.strip() for li in language_section.find_all('li')] if language_section else []
    cv_data["languages"] = languages
    print(cv_data)
    return cv_data

def get_doctor_details(url):
    soup = get_soup(url)
    doctor = {}

    doctor['name'] = re.search(r'/([^/]+)/[^/]+/[^/]+$', url).group(1)
    

    location_elements = soup.select('div[data-doctor-stats="contact"] a')
    location_urls = [location['href'] for location in location_elements]
    parsed_urls = [urlparse(url) for url in location_urls]
    query_params = [parse_qs(parsed_url.query) for parsed_url in parsed_urls]
    lat_longs = [query_param['query'][0].split(',') for query_param in query_params]
    doctor['location'] = lat_longs


    service_elements = soup.select('p[itemprop="availableService"]')
    doctor['services'] = [service.text.strip() for service in service_elements]

    phone_element = soup.select_one('i.svg-icon-phone')
    doctor['phone'] = phone_element.parent.text.strip() if phone_element else None
    insurance_elements = soup.select('div.p-2 h5 a')
    doctor['accepted_insurances'] = [insurance.text.strip() for insurance in insurance_elements]

    photo_element = soup.select_one('div[data-image-gallery="true"] img')
    doctor['photo'] = photo_element['src'] if photo_element else None

    doctor['experience'] = "0"

    # Scrape CV details
    doctor['cv'] = scrape_cv(soup.prettify())

    return doctor

def scrape_doctors(specialization, location):
    url = f'{BASE_URL}{specialization}/{location}'
    
    soup = get_soup(url)

    doctor_elements = soup.select('h3.h4.mb-0.flex-wrap a')
    
    doctor_links = [element['href'] for element in doctor_elements]
    doctors = []
    for link in doctor_links:
        doctor = get_doctor_details(link)

        db_doctor = Doctor(name=doctor['name'], phone=doctor['phone'], specialty=specialization, institution=Institution.objects.get_or_create(name=location,location=doctor['location'])[0])
        db_doctor.photo = doctor['photo']
        cv_data = doctor['cv']
        db_cv = Cv(educations=cv_data['educations'], languages=cv_data['languages'], interests=cv_data['interests'], about=cv_data['about'])
        db_cv.save()
        db_doctor.cv = db_cv
        doctors.append(doctor)
        db_doctor.save()

        for service_name in doctor['services']:
            print(service_name)
            service = Services.objects.get_or_create(name=service_name)[0]
            db_doctor.services.add(service)

        for insurance_name in doctor['accepted_insurances']:
            insurance = Insurance.objects.get_or_create(name=insurance_name)[0]
            db_doctor.accepted_insurance_providers.add(insurance)
        # Create CV and link it to the doctor
       

    
    return doctors

def scrape_doctors_endpoint(request):
    specialization = request.GET.get('spec')
    location = request.GET.get('localization')

    if specialization and location:
        doctors = scrape_doctors(specialization, location)
        return JsonResponse({'doctors': doctors})
    else:
        return JsonResponse({'error': 'Missing parameters: spec, localization'})
