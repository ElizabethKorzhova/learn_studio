from ls.models import Notification


def create_notification(user, message: str, type_: str):
    """Create a new notification
    """
    return Notification.objects.create(
        user=user,
        message=message,
        type=type_
    )
