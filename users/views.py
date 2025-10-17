from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

# Create your views here.
def landing_page(request):
    return render(request, 'users/landing.html', {'mode': None})

def login(request):
    return render(request, 'users/login.html', {'mode': 'login'})

def signup(request):
    return render(request, 'users/login.html', {'mode': 'signup'})

def dashboard(request):
    return HttpResponse(f"<h1>Dashboard</h1><p>User: {request.user.username}</p>")

def in_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

@user_passes_test(lambda u: in_group(u, "user"))
def user_only(request):
    return HttpResponse("<h1>User Area</h1>")

@user_passes_test(lambda u: in_group(u, "admin"))
def admin_only(request):
    return HttpResponse("<h1>Admin Area</h1>")

def my_profile(request):
    # Minimal profile page using built-in User fields
    return HttpResponse(f"<h1>My Profile</h1><p>{request.user.username}</p>")

def user_profile(request, username):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("<h1>User not found</h1>", status=404)
    return HttpResponse(f"<h1>Profile: {u.username}</h1>")

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