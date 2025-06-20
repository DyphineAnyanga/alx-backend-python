from django.db import models
from django.contrib.auth.models import User

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return super().get_queryset().filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')
