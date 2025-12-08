from django.db import models
from django.contrib.auth.models import User
from postman.models import Message

# Create your models here.

class GroupChat(models.Model):
    name = models.CharField(max_length=150)
    members = models.ManyToManyField(User, related_name='group_chats')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class GroupChatMessage(models.Model):
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    postman = models.ManyToManyField(Message, blank=True) 