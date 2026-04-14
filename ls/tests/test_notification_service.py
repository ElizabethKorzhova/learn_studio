import pytest
from ls.models import Notification
from ls.services.notification_service import create_notification


@pytest.mark.django_db
def test_create_notification(user_factory):
    """test create notification
    """
    user = user_factory()

    notification = create_notification(
        user=user,
        message="Test message",
        type_="message"
    )

    assert notification is not None
    assert notification.user == user
    assert notification.message == "Test message"
    assert Notification.objects.count() == 1
