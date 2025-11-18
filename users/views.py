from django.contrib import messages
from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import logout as user_logout
from allauth.socialaccount.models import *

from django.core.files.storage import default_storage
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# email verification
from django.core import signing
from django.utils import timezone
from datetime import timedelta
from .forms import StudentEmailForm
from django.core.mail import send_mail
from django.template.loader import render_to_string


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

@login_required
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
            if(request.POST.get("nickname", cur_user.username)):       
                cur_user.profile.nickname = request.POST.get("nickname", cur_user.profile.nickname)
            if(request.POST.get("email", cur_user.email)):
                cur_user.email = request.POST.get("email", cur_user.email)
            # save photo if user has Profile class
            if(request.FILES.get('profile_photo')):
                cur_user.profile.image = request.FILES.get('profile_photo')
                print('image: ', cur_user.profile.image)
            cur_user.profile.save()
            cur_user.save()
            return redirect("my_profile")
    return redirect('my_profile')

@login_required
def delete_profile(request):
    user = request.user
    user.delete()

    return redirect("/")

# helper functions to generate and verify email tokens
def generate_student_token(user):
    token_data = {
        'user_id': user.id,
        'timestamp': str(timezone.now()),
        'email': user.profile.student_email
    }
    token = signing.dumps(token_data)
    return token

def verify_student_token(token, max_age=3600):
    try:
        token_data = signing.loads(token, max_age=max_age)
        return token_data
    except signing.BadSignature:
        return None
    
# view to handle sending verification email
@login_required
def request_student_verification(request):
    user = request.user
    if request.method == "POST":
        form = StudentEmailForm(request.POST)
        if form.is_valid():
            user.profile.student_email = form.cleaned_data['student_email']
            user.profile.student_email_verified = False
            user.profile.save()

            token = generate_student_token(user)
            verification_link = request.build_absolute_uri(
                reverse('verify_student_email', kwargs={'token': token})
            )

            html_message = render_to_string("users/student_verification_email.html", {
                'user': user,
                'link': verification_link
            })

            send_mail(
                subject="Verify your UVA Student Email",
                message="Please verify your student email by clicking the link below.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.profile.student_email],
                html_message=html_message,
            )

            messages.success(request, "Verification email sent. Please check your inbox.")
            return redirect("my_profile")
    else:
        form = StudentEmailForm(initial={'student_email': user.profile.student_email})

    return render(request, "users/student_email_form.html", {'form': form})

# view to confirm the token
def verify_student_email(request, token):
    data = verify_student_token(token)
    if not data or int(data['user_id']) != request.user.id:
        messages.error(request, "Invalid or expired verification link.")
        return redirect("my_profile")

    request.user.profile.student_email_verified = True
    request.user.profile.save()
    messages.success(request, "Your student email has been verified.")
    return redirect("my_profile")