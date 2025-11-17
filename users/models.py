from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_suspended = models.BooleanField(default=False)
    image = ProcessedImageField(upload_to='profile_pics',
                                default='profile_pics/default.jpg',
                                processors=[ResizeToFill(200, 200)],
                                format='JPEG',
                                options={'quality': 60})

    def __str__(self):
        return self.user.username