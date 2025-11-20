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

def suspended(request):
    return render(request, 'login/suspended.html', {'mode': None})

def appeal(request):
    action = request.POST.get('action')

    if action:
        if action == 'submitAppeal':
            pass #Add stuff here to save to an appeals model, have the text stored, and for other view only let them click button if they haven't already appealed.
    return render(request, 'login/appeal.html', {'mode': None})

def logout(request):
    user_logout(request)
    return redirect('/')
