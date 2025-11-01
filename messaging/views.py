from django.shortcuts import *
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import logout as user_logout
from allauth.socialaccount.models import *
# Create your views here.

def get_mode(request):
    return 'admin' if request.user.is_superuser else 'user'

@login_required
def messages_overview(request):
    return render(request, 'messaging/message_overview.html', {'mode': get_mode(request)})