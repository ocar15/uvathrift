import requests
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile
from allauth.socialaccount.models import SocialAccount
from django.core.files.base import ContentFile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    profile, created = Profile.objects.get_or_create(user=instance)
    profile.save()

@receiver(post_save, sender=SocialAccount)
def add_default_google_info(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    name = instance.extra_data.get('name')
    image_url = instance.extra_data.get('picture')

    try:
        response = requests.get(image_url)
        response.raise_for_status()
    except requests.RequestException:
        return
    
    profile, created = Profile.objects.get_or_create(user=user)

    file = f"{user.username}_google.jpg"
    profile.image.save(file, ContentFile(response.content), save=True)

    user.profile.display_name = name
    user.profile.nickname = name

    user.save()
    user.profile.save()