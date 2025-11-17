from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
from django.utils import timezone


class SuspendedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            profile = user.profile
            if profile.suspended_until and timezone.now() >= profile.suspended_until:
                profile.suspended_until = None
                profile.save()
            
            if profile.is_suspended():
                exclusions = [reverse('suspended'),reverse('logout')]
                if request.path not in exclusions:
                    return redirect('suspended')
                
        return self.get_response(request)