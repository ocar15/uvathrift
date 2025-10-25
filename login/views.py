from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import logout as user_logout
from allauth.socialaccount.models import *




# Create your views here.
def landing_page(request):
    return render(request, 'login/landing.html', {'mode': None})

def login(request):
    return render(request, 'login/login.html', {'mode': 'login'})

def signup(request):
    return render(request, 'login/login.html', {'mode': 'signup'})