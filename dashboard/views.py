from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import logout as user_logout
from allauth.socialaccount.models import *



def super_user_required(func):
    return user_passes_test(lambda u: u.is_superuser, login_url='dashboard')(func)

def get_mode(request):
    return 'admin' if request.user.is_superuser else 'user'

# Create your views here.

def logout(request):
    user_logout(request)
    return redirect('/')


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {'mode': get_mode(request)})


def items_list(request):
     return HttpResponse("")

def item_create(request):
     return HttpResponse("")

def cart(request):
     return HttpResponse("")

def checkout(request):
     return HttpResponse("")

def orders(request):
     return HttpResponse("")