from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                # Create a history entry before the message is updated
                MessageHistory.objects.create(
                    message=original,
                    old_content=original.content,
                    edited_by=instance.edited_by,
                )
                instance.edited = True
                instance.edited_at = timezone.now()
        except Message.DoesNotExist:
            pass
