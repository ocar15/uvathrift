from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import logout as user_logout
from allauth.socialaccount.models import *

from io import BytesIO

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
    user_data = None

    try:
        user = SocialAccount.objects.get(user=request.user)
        user_data = user.extra_data
    except SocialAccount.DoesNotExist:
        user_data = "Invalid User"

    return render(request, 'users/edit-profile.html', {'user_data': user_data, 'mode': get_mode(request)})


@api_view(('GET',))
def save_file(request):
    file_name = "test.txt"
    file_content = b"this is a test"
    file_content_io = BytesIO(file_content)

    default_storage.save(file_name, file_content_io)

    return Response({"message": "File successfully saved"})