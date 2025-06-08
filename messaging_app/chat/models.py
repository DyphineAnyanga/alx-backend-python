from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Extend if you want, else use Django's built-in User directly
    pass

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'From {self.sender.username} to {self.recipient.username} at {self.timestamp}'
