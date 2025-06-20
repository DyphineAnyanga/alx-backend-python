from django.db.models.signals import post_save
from django.dispatch import receiver
from messaging.models import Message, Notification


@receiver(post_save, sender=Message)
def notify_receiver(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
