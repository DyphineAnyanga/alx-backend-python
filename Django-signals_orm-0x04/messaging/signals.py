from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Track and log message edits before saving."""
    if instance.pk:
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                MessageHistory.objects.create(
                    message=original,
                    previous_content=original.content,
                    edited_at=now(),
                    edited_by=instance.user
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """Delete messages, notifications, and history when a user is deleted."""
    Message.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
    Notification.objects.filter(user=instance).delete()

