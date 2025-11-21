from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Appeals(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='appeals')
    appeal = models.TextField()
    choices = [('A', "Approved"), ('D', "Declined"), ('P', "Pending")]
    status = models.CharField(max_length=20, choices=choices ,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appeal from {self.user.username} status: {self.status}"

