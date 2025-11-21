from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from moderation.models import Appeals
from django.contrib.auth import logout as user_logout
from allauth.socialaccount.models import *




# Create your views here.
def landing_page(request):
    return render(request, 'login/landing.html', {'mode': None})

def login(request):
    return render(request, 'login/login.html', {'mode': 'login'})

def signup(request):
    return render(request, 'login/login.html', {'mode': 'signup'})

def suspended(request):
    return render(request, 'login/suspended.html', {'mode': None})

def appeal(request):
    action = request.POST.get("action")
    if request.method == "POST":
        cur_userid = request.user.id
        if not cur_userid:
            return redirect("suspended")
        try:
            cur_user = User.objects.get(id=cur_userid)
        except User.DoesNotExist:
            return redirect("suspended")
        if action == 'submitAppeal':
            
            appeal = request.POST.get('appeal', '').strip()

            Appeals.objects.create(user=cur_user, appeal=appeal)
            return render(request, 'login/appeal_submitted.html')
        if action == 'appeal':
            if hasattr(cur_user, 'appeals') and cur_user.appeals.status in ['Pending', 'Declined'] :
                return render(request, 'login/already_appealed.html', {'status': Appeals.objects.get(user_id=request.user.id).status})
            return render(request, 'login/appeal.html')
    return redirect('suspended')

def logout(request):
    user_logout(request)
    return redirect('/')
