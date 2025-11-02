from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import UserProfile

# reads that a new user has signed up, processes them
@receiver(user_signed_up)
def handle_user_signed_up(request, sociallogin, user, **kwargs):

    # grab the user's data
    new_user_data = sociallogin.account.extra_data
    
    print(new_user_data)

    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.is_suspended = False
    profile.save()

    # perform tasks/processing on data