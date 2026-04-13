import pytest
from rest_framework import status

from ls.models import Transaction, Enrollment


@pytest.fixture
def course(instructor_user):
    """Creates a sample course for testing purposes
    """
    return instructor_user.courses.create(
        title="Django Pro",
        description="Advanced course",
        price=100.00,
        start_at="2026-01-01T00:00:00Z",
        duration=10
    )


@pytest.fixture
def another_user(django_user_model):
    """Creates an additional user for testing access control scenarios
    """
    return django_user_model.objects.create_user(
        email="another@test.com",
        username="another",
        password="password123",
        role="student"
    )


@pytest.mark.django_db
def test_create_transaction_success(api_client, student_user, course):
    """Tests successful creation of a transaction
    """
    api_client.force_authenticate(user=student_user)

    response = api_client.post(
        "/api/transactions/",
        {"course": course.id},
        format="json"
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_transaction_already_purchased(api_client, student_user, course):
    """Tests prevention of duplicate successful transactions
    """
    Transaction.objects.create(
        user=student_user,
        course=course,
        amount=100.00,
        status="success",
        payment_data={}
    )

    api_client.force_authenticate(user=student_user)

    response = api_client.post(
        "/api/transactions/",
        {"course": course.id},
        format="json"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_list_transactions_only_own(api_client, student_user, another_user, course):
    """Tests that a user can only see their own transactions
    """
    own_transaction = Transaction.objects.create(
        user=student_user,
        course=course,
        amount=100.00,
        status="pending",
        payment_data={}
    )

    Transaction.objects.create(
        user=another_user,
        course=course,
        amount=100.00,
        status="pending",
        payment_data={}
    )

    api_client.force_authenticate(user=student_user)

    response = api_client.get("/api/transactions/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == own_transaction.id


@pytest.mark.django_db
def test_confirm_transaction_success(api_client, student_user, course):
    """Tests successful confirmation of a transaction
    """
    transaction = Transaction.objects.create(
        user=student_user,
        course=course,
        amount=100.00,
        status="pending",
        payment_data={}
    )

    api_client.force_authenticate(user=student_user)

    response = api_client.post(
        f"/api/transactions/{transaction.id}/confirm/",
        {"payment_data": {"id": "pi_123"}},
        format="json"
    )

    assert response.status_code == status.HTTP_200_OK

    transaction.refresh_from_db()
    assert transaction.status == "success"

    assert Enrollment.objects.filter(
        user=student_user,
        course=course
    ).exists()


@pytest.mark.django_db
def test_confirm_transaction_not_owner(api_client, student_user, another_user, course):
    """Tests that a user cannot confirm another user's transaction
    """
    transaction = Transaction.objects.create(
        user=student_user,
        course=course,
        amount=100.00,
        status="pending",
        payment_data={}
    )

    api_client.force_authenticate(user=another_user)

    response = api_client.post(
        f"/api/transactions/{transaction.id}/confirm/",
        {"payment_data": {}},
        format="json"
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
