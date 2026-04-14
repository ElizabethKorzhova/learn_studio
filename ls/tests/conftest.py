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
        deadline_date="2026-01-10",
        complexity=1
    )


@pytest.fixture
def enrollment(student_user, course):
    return Enrollment.objects.create(
        user=student_user,
        course=course,
        course_status="active"
    )






@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        return User.objects.create_user(
            email=kwargs.get("email", "test@test.com"),
            username=kwargs.get("username", "test"),
            password="pass",
            role=kwargs.get("role", "student")
        )
    return create_user


@pytest.fixture
def course_factory(db):
    def create_course(instructor=None):
        if not instructor:
            instructor = User.objects.create_user(
                email="inst@test.com",
                username="inst",
                password="pass",
                role="instructor"
            )

        return Course.objects.create(
            instructor=instructor,
            title="Test Course",
            description="Test",
            price=100,
            start_at="2026-01-01T00:00:00Z",
            duration=10
        )

    return create_course

@pytest.fixture
def submission_factory(user_factory, course_factory):
    def create_submission(**kwargs):
        user = user_factory()
        course = course_factory()

        lesson = course.lessons.create(
            title="Lesson 1",
            content="Test",
            order_index=1
        )

        homework = lesson.homeworks.create(
            title="HW",
            task="Test task",
            deadline="2026-01-01T00:00:00Z",
            complexity=1,
            created_by=user,
            deadline_date="2026-01-01"
        )

        return HomeworkSubmission.objects.create(
            user=user,
            homework=homework,
            **kwargs
        )

    return create_submission