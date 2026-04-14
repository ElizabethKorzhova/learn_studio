from django.db.models.signals import post_save
from django.dispatch import receiver
from ls.models import Notification, Message


@receiver(post_save, sender=Message)
def notify_message(sender, instance, created, **kwargs):
    """Notify new message
    """
    if not created:
        return

    submission = instance.homework_submission
    receiver = submission.user

    if instance.sender == receiver:
        return

    Notification.objects.create(
        user=receiver,
        title="New message",
        message=instance.message_text[:100],
        type="message",
        related_id=submission.id
    )
