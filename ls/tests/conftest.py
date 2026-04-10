import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from datetime import datetime, timezone

from ls.models import Course
from ls.models import Lesson
from ls.models import HomeworkSubmission, Homework, Enrollment
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    """api client
    """
    return APIClient()


@pytest.fixture
def admin_user(db) -> User:
    """admin user
    """
    return User.objects.create_user(
        email="admin@test.com",
        username="admin",
        password="pass1234",
        role="admin",
        first_name="Admin",
        last_name="User"
    )


@pytest.fixture
def instructor_user(db) -> User:
    """instructor user
    """
    return User.objects.create_user(
        email="inst@test.com",
        username="inst",
        password="pass1234",
        role="instructor",
        first_name="Instructor",
        last_name="User"
    )


@pytest.fixture
def student_user(db) -> User:
    """student user
    """
    return User.objects.create_user(
        email="student@test.com",
        username="student",
        password="pass1234",
        role="student",
        first_name="Student",
        last_name="User"
    )


@pytest.fixture
def course(instructor_user) -> Course:
    """course
    """
    return Course.objects.create(
        instructor=instructor_user,
        title="Math",
        description="Basic math course",
        price=100,
        start_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        duration=10
    )


@pytest.fixture
def get_token():
    def _get_token(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    return _get_token


@pytest.fixture
def auth_client(api_client, get_token):
    """auth client
    """

    def _auth(user) -> APIClient:
        token = get_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return api_client

    return _auth


@pytest.fixture
def lesson(course):
    """lesson
    """
    return Lesson.objects.create(
        course=course,
        title="Algebra 1",
        content="Intro to algebra",
        order_index=1
    )


@pytest.fixture
def submission(homework, student_user):
    """submission
    """
    return HomeworkSubmission.objects.create(
        homework=homework,
        student=student_user,
        text_answer="My solution",
        score=None
    )


@pytest.fixture
def homework(lesson):
    """homework
    """
    return Homework.objects.create(
        lesson=lesson,
        title="Test HW",
        task="Solve it",
        deadline="2026-01-10T10:00:00Z",
        complexity=1
    )
