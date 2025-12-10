from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    new_user = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False)
    suspended_until = models.DateTimeField(null=True, blank=True)
    nickname = models.CharField("nickname", max_length=50, blank=True)
    bio = models.CharField("bio", max_length=300, blank=True)
    image = ProcessedImageField(upload_to='profile_pics',
                                default='profile_pics/default.jpg',
                                processors=[ResizeToFill(200, 200)],
                                format='JPEG',
                                options={'quality': 60})
    student_email = models.EmailField(null=True, blank=True)
    student_email_verified = models.BooleanField(default=False)
    display_name = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.user.username
        super().save(*args, **kwargs)
    def is_suspended(self):
        return self.suspended_until is not None and timezone.now() < self.suspended_until
    @property
    def remaining_time(self):
        if not self.suspended_until or timezone.now() >= self.suspended_until:
            return None

        time_left = self.suspended_until - timezone.now()
        days = time_left.days
        hours = time_left.seconds // 3600
        minutes = (time_left.seconds % 3600) // 60

        if days > 0:
            return f"{days} day{'s' if days != 1 else ''} remaining"
        elif hours > 0:
            return f"{hours} hour{'s' if hours != 1 else ''} remaining"
        else:
            return f"{minutes} minute{'s' if minutes != 1 else ''} remaining"
        

    def __str__(self):
        return self.user.username