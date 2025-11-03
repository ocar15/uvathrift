from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse


class SuspendedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            if request.user.profile.is_suspended:
                logout(request)

                if request.path != reverse('suspended'):
                    return redirect('suspended')
                
        return self.get_response(request)