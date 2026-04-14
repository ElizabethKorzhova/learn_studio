from django.db.models.signals import post_save
from django.dispatch import receiver
from ls.models import Notification, Transaction


@receiver(post_save, sender=Transaction)
def notify_payment(sender, instance, created, **kwargs):
    """Notify new payment
    """
    if instance.status != "success":
        return

    Notification.objects.create(
        user=instance.user,
        title="Payment successful",
        message=f"You enrolled in {instance.course.title}",
        type="payment",
        related_id=instance.course.id
    )
