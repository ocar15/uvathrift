from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from .models import *
from dashboard.models import Item
from django.contrib.auth import logout as user_logout
from allauth.socialaccount.models import *
from datetime import datetime
from django.utils import timezone
from django.db.models import Count






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
    query = request.GET.get('q', '').strip().lower()
    users = User.objects.all()
    user_info = []
    for u in users:
        try:
            social = SocialAccount.objects.filter(user=u).first()
            user_data = social.extra_data
        except SocialAccount.DoesNotExist:
            user_data = {}


        if (query in u.username.lower() or query in u.profile.nickname.lower() or query in u.email.lower()):
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
            cur_user.profile.nickname = request.POST.get("username", cur_user.profile.nickname)
            cur_user.email = request.POST.get("email", cur_user.email)
            cur_user.is_superuser = bool(request.POST.get("is_superuser"))
            cur_user.is_staff = bool(request.POST.get("is_superuser"))
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
                try:
                    appeal = Appeals.objects.get(user_id=cur_user.id)
                    appeal.delete()
                except:
                    pass
            return redirect('manage_users')
        elif action == 'end_suspension':
            cur_user.profile.suspended_until = None
            cur_user.profile.save()
            cur_user.profile.refresh_from_db()
       
    return redirect("manage_users")

@super_user_required
def manage_appeals(request):
    appeals = Appeals.objects.all()
    users = User.objects.all()
    user_info = []
    for u in appeals:
        if u.status in ["Declined", "Approved"]:
            continue
        try:
            social = SocialAccount.objects.get(user=u.user)
            user_data = social.extra_data
        except SocialAccount.DoesNotExist:
            user_data = {}


        user_info.append({
            "user": u.user,
            "data": user_data,
        })
    return render(request, 'moderation/manage_appeals.html', {'users': users, 'mode': get_mode(request), 'user_data': user_info})


@super_user_required
def view_appeal(request):
    action = request.POST.get("action")
    cur_userid = request.POST.get('user_id')
    user_info = {}
    if request.method == "POST":
        cur_user = User.objects.get(id=cur_userid)
        if action == 'viewAppeal':
            try:
                social = SocialAccount.objects.get(user=cur_user)
                user_data = social.extra_data
            except SocialAccount.DoesNotExist:
                user_data = {}


            user_info= {
            "user": cur_user,
            "data": user_data,
            "appeal": Appeals.objects.get(user=cur_user).appeal,
            }
            return render(request, 'moderation/view_appeal.html', {'mode': get_mode(request), 'user_data': user_info})
        if action == 'acceptAppeal':
            appeal = Appeals.objects.get(user_id=cur_userid)
            try:
                appeal.delete()
            except:
                pass
            cur_user.profile.suspended_until = None
            cur_user.profile.save()
            cur_user.profile.refresh_from_db()
        if action == 'declineAppeal':
            appeal = Appeals.objects.get(user_id=cur_userid)
            appeal.status = "Declined"
            appeal.save()
    return redirect('manage_appeals')


@super_user_required
def manage_posts(request):
    reports = Reports.objects.all()
    reports = Reports.objects.values('item').annotate(report_count=Count('id'))
    report_info = []
    for report in reports:
        item = Item.objects.get(pk=report['item'])
        report_info.append({
            "item": item,
            "report_count": report['report_count'],
        })
    return render(request, "moderation/manage_posts.html", {'mode': get_mode(request), 'report_info': report_info})

@super_user_required
def view_report(request, pk):
    action = request.POST.get("action")
    item = get_object_or_404(Item, pk=pk)
    reports = Reports.objects.filter(item=item)

    if action:
        if action == "ignore":
            Reports.objects.filter(item=item).delete()
            return redirect("manage_posts")
        elif action == "removePost":
            Reports.objects.filter(item=item).delete()
            item.delete()
            return redirect("manage_posts")
        elif action == "cancel":
            return redirect("manage_posts")

    return render(request, 'moderation/view_report.html', {'mode': get_mode(request), 'reports': reports, "item": item})


@super_user_required
def analytics(request):
    return redirect("admin_only")
