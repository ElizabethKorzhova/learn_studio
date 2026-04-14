import pytest
from ls.models import Transaction, Enrollment
from ls.services.payment_service import confirm_payment


@pytest.mark.django_db
def test_confirm_payment_creates_enrollment(user_factory, course_factory):
    """test confirm_payment creates enrollment
    """
    user = user_factory()
    course = course_factory()

    transaction = Transaction.objects.create(
        user=user,
        course=course,
        amount=100,
        status="pending",
        payment_data={}
    )

    confirm_payment(transaction)

    transaction.refresh_from_db()

    assert transaction.status == "success"
    assert Enrollment.objects.filter(user=user, course=course).exists()
