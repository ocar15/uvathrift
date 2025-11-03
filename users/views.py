from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import logout as user_logout
from allauth.socialaccount.models import *

from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework.response import Response


def get_mode(request):
    return 'admin' if request.user.is_superuser else 'user'

# Create your views here.

def logout(request):
    user_logout(request)
    return redirect('/')


def in_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

@user_passes_test(lambda u: in_group(u, "user"))
def user_only(request):
    return HttpResponse("<h1>User Area</h1>")


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

    return render(request, 'users/profile.html', {'user_data': user_data, 'mode': get_mode(request)})

def user_profile(request, username):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("<h1>User not found</h1>", status=404)
    return HttpResponse(f"<h1>Profile: {u.username}</h1>")

def edit_profile(request):
    action = request.POST.get("action")
    if request.method == "POST":
        cur_userid = request.POST.get("user_id")
        if not cur_userid:
            return redirect("my_profile")
        try:
            cur_user = User.objects.get(id=cur_userid)
        except User.DoesNotExist:
            return redirect("my_profile")

        if action == 'edit':
            return render(request, 'users/edit_profile.html', {'user': cur_user, 'mode': get_mode(request)})

        elif action == 'save':
            if(request.POST.get("username", cur_user.username)):       
                cur_user.username = request.POST.get("username", cur_user.username)
            if(request.POST.get("email", cur_user.email)):
                cur_user.email = request.POST.get("email", cur_user.email)
            # save photo if user has Profile class
            if(request.FILES.get('profile_photo')):
                cur_user.profile.image = request.FILES.get('profile_photo')
                cur_user.profile.save()
            cur_user.save()
            print('image: ', cur_user.profile.image)
            return redirect("my_profile")
    return redirect('my_profile')