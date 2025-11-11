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
@super_user_required
def admin_only(request):
    return render(request, 'moderation/administrator.html', {'mode': get_mode(request)})

@super_user_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'moderation/manage_users.html', {'users': users, 'mode': get_mode(request)})

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
            return render(request, 'moderation/edit_user.html', {'edit_user': cur_user, 'mode': get_mode(request)})
        
        elif action == 'save':            
            cur_user.username = request.POST.get("username", cur_user.username)
            cur_user.email = request.POST.get("email", cur_user.email)
            cur_user.is_superuser = bool(request.POST.get("is_superuser"))
            cur_user.profile.is_suspended = bool(request.POST.get("is_suspended"))
            cur_user.save()
            cur_user.profile.save()
            return redirect("manage_users")
        
    return redirect("manage_users")

@super_user_required
def manage_posts(request):
    return redirect("admin_only")

@super_user_required
def analytics(request):
    return redirect("admin_only")