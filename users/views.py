from django.shortcuts import render

# Create your views here.
def landing_page(request):
    return render(request, 'users/landing.html', {'mode': None})

def login(request):
    return render(request, 'users/login.html', {'mode': 'login'})

def signup(request):
    return render(request, 'users/login.html', {'mode': 'signup'})