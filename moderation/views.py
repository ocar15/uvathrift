from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import logout as user_logout
from allauth.socialaccount.models import *
from datetime import datetime
from django.utils import timezone






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
    user_info = []
    for u in users:
        try:
            social = SocialAccount.objects.get(user=u)
            user_data = social.extra_data
        except SocialAccount.DoesNotExist:
            user_data = {}


        user_info.append({
            "user": u,
            "data": user_data
        })
    return render(request, 'moderation/manage_users.html', {'users': users, 'mode': get_mode(request), 'user_data': user_info})


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
       
        elif action == 'cancel':
            redirect('manage_users')


        elif action == 'save':            
            cur_user.username = request.POST.get("username", cur_user.username)
            cur_user.email = request.POST.get("email", cur_user.email)
            cur_user.is_superuser = bool(request.POST.get("is_superuser"))
            # cur_user.profile.is_suspended = bool(request.POST.get("is_suspended"))
            cur_user.save()
            cur_user.profile.save()
            return redirect("manage_users")
        elif action == 'suspend':
            suspend = None
            if cur_user.profile.suspended_until:
                time = timezone.localtime(cur_user.profile.suspended_until)
                suspend = time.strftime("%Y-%m-%dT%H:%M")
            return render(request, 'moderation/edit_suspension.html', {'user': cur_user, 'mode': get_mode(request), 'suspended_date': suspend})
        elif action == 'suspend_save':
            suspended_until = request.POST.get('suspension_date')
            if suspended_until:
                suspended_until = datetime.fromisoformat(suspended_until)
                suspended_until = timezone.make_aware(suspended_until, timezone.get_current_timezone())


                cur_user.profile.suspended_until = suspended_until
                cur_user.profile.save()
            return redirect('manage_users')
        elif action == 'end_suspension':
            cur_user.profile.suspended_until = None
            cur_user.profile.save()
            cur_user.profile.refresh_from_db()
       
    return redirect("manage_users")


@super_user_required
def manage_posts(request):
    return redirect("admin_only")


@super_user_required
def analytics(request):
    return redirect("admin_only")
