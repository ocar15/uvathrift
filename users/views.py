from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import logout as user_logout
from allauth.socialaccount.models import *



def super_user_required(func):
    return user_passes_test(lambda u: u.is_superuser, login_url='dashboard')(func)

# Create your views here.
def landing_page(request):
    return render(request, 'users/landing.html', {'mode': None})

def login(request):
    return render(request, 'users/login.html', {'mode': 'login'})

def logout(request):
    user_logout(request)
    return redirect('/')

def signup(request):
    return render(request, 'users/login.html', {'mode': 'signup'})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        mode = 'admin'
    else:
        mode = 'user'
    return render(request, 'users/dashboard.html', {'mode': mode})

def in_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

@user_passes_test(lambda u: in_group(u, "user"))
def user_only(request):
    return HttpResponse("<h1>User Area</h1>")

@login_required
@super_user_required
def admin_only(request):
    return render(request, 'users/administrator.html', {'mode': 'admin' if request.user.is_superuser else 'user'})

@super_user_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'users/manage_users.html', {'users': users})

@super_user_required
def edit_user(request):
    action = request.POST.get("action")
    if request.method == "POST":
        cur_userid = request.POST.get("user_id")
        if not cur_userid:
            return redirect("manage_users")
        try:
            cur_user = User.objects.get(id=cur_userid)
        except User.DoesNotExist:
            return redirect("manage_users")
        
        if action == 'edit':
            return render(request, 'users/edit_user.html', {'user': cur_user})
        
        elif action == 'save':            
            cur_user.username = request.POST.get("username", cur_user.username)
            cur_user.email = request.POST.get("email", cur_user.email)
            cur_user.is_superuser = bool(request.POST.get("is_superuser"))
            cur_user.save()
            return redirect("manage_users")
        
    return redirect("manage_users")

@login_required
def my_profile(request):
    # Minimal profile page using built-in User fields
    # return HttpResponse(f"<h1>My Profile</h1><p>{request.user.username}</p>")
    user_data = None

    try:
        user = SocialAccount.objects.get(user=request.user)
        user_data = user.extra_data
    except SocialAccount.DoesNotExist:
        user_data = "Invalid User"

    return render(request, 'users/profile.html', {'user_data': user_data, 'mode': 'admin' if request.user.is_superuser else 'user'})

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