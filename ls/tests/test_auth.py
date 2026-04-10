import pytest
from rest_framework.test import APIClient
from ls.models import User


@pytest.mark.django_db
def test_register_user():
    """ Test that a user can be registered
    """
    client = APIClient()

    payload = {
        "email": "test@test.com",
        "username": "testuser",
        "password": "12345678",
        "first_name": "Test",
        "last_name": "User",
        "role": "student"
    }

    response = client.post("/api/auth/register/", payload)

    assert response.status_code == 201
    assert "access" in response.data
    assert User.objects.filter(email="test@test.com").exists()


@pytest.mark.django_db
def test_login_user():
    """ Test that a user can be logged in
    """
    client = APIClient()

    user = User.objects.create_user(
        email="test@test.com",
        username="testuser",
        password="12345678",
        role="student"
    )

    response = client.post("/api/auth/login/", {
        "email": "test@test.com",
        "password": "12345678"
    })

    assert response.status_code == 200
    assert "access" in response.data
