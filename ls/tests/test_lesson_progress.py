import pytest
from rest_framework.test import APIClient
from django.utils.timezone import now

from ls.models import User, Course, Lesson, Enrollment, LessonProgress


@pytest.fixture
def client():
    """Initializes the API client for testing.
    """
    return APIClient()


@pytest.fixture
def student(django_user_model):
    """Creates a user with the 'student' role.
    """
    return django_user_model.objects.create_user(
        username="student",
        email="student@test.com",
        password="pass1234",
        role="student"
    )


@pytest.fixture
def instructor(django_user_model):
    """Creates a user with the 'instructor' role.
    """
    return django_user_model.objects.create_user(
        username="instructor",
        email="inst@test.com",
        password="pass1234",
        role="instructor"
    )


@pytest.fixture
def course(instructor):
    """Creates a test course assigned to an instructor.
    """
    return Course.objects.create(
        instructor=instructor,
        title="Test Course",
        description="Desc",
        price=100,
        start_at=now(),
        duration=10
    )


@pytest.fixture
def lessons(course):
    """Creates a set of lessons for the given course.
    """
    return [
        Lesson.objects.create(course=course, title="L1", content="...", order_index=1),
        Lesson.objects.create(course=course, title="L2", content="...", order_index=2),
    ]


@pytest.fixture
def enrollment(student, course):
    """Enroll a student in a course.
    """
    return Enrollment.objects.create(user=student, course=course)


@pytest.mark.django_db
def test_create_lesson_progress(client, student, lessons, enrollment):
    """Test successful creation of lesson progress via POST request.
    Verifies that 'is_completed' is set and 'completed_at' timestamp is generated.
    """
    client.force_authenticate(user=student)

    url = "/api/lesson-progress/"

    response = client.post(url, {
        "lesson": lessons[0].id,
        "is_completed": True
    })

    assert response.status_code == 201
    progress = LessonProgress.objects.get(user=student, lesson=lessons[0])
    assert progress.is_completed is True
    assert progress.completed_at is not None


@pytest.mark.django_db
def test_update_lesson_progress(client, student, lessons, enrollment):
    """Test updating an existing lesson progress record via PATCH.
    Ensures that the status changes correctly in the database.
    """
    progress = LessonProgress.objects.create(
        user=student,
        lesson=lessons[0],
        is_completed=False
    )

    client.force_authenticate(user=student)
    url = f"/api/lesson-progress/{progress.id}/"

    response = client.patch(url, {"is_completed": True})

    assert response.status_code == 200
    progress.refresh_from_db()
    assert progress.is_completed is True


@pytest.mark.django_db
def test_course_progress_updates(client, student, lessons, enrollment):
    """Test that completing one lesson updates the overall course progress percentage.
    In a 2-lesson course, completing 1 lesson should result in 50% progress.
    """
    client.force_authenticate(user=student)

    client.post("/api/lesson-progress/", {
        "lesson": lessons[0].id,
        "is_completed": True
    })

    enrollment.refresh_from_db()
    assert enrollment.user_progress == 50


@pytest.mark.django_db
def test_full_course_completion(client, student, lessons, enrollment):
    """Test that completing all lessons in a course results in 100% progress.
    """
    client.force_authenticate(user=student)

    for lesson in lessons:
        client.post("/api/lesson-progress/", {
            "lesson": lesson.id,
            "is_completed": True
        })

    enrollment.refresh_from_db()
    assert enrollment.user_progress == 100


@pytest.mark.django_db
def test_user_sees_only_own_progress(client, student, instructor, lessons):
    """Ensure the API filters results so users can only see their own progress records.
    """
    LessonProgress.objects.create(user=instructor, lesson=lessons[0])

    client.force_authenticate(user=student)
    response = client.get("/api/lesson-progress/")

    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_unique_lesson_progress(student, lessons):
    """Verify database-level constraints: a user cannot have duplicate progress
    records for the same lesson.
    """
    LessonProgress.objects.create(user=student, lesson=lessons[0])

    with pytest.raises(Exception):
        LessonProgress.objects.create(user=student, lesson=lessons[0])


@pytest.mark.django_db
def test_create_progress_twice(client, student, lessons, enrollment):
    """Test 'get_or_create' logic in the ViewSet.
    Sending multiple POST requests for the same lesson should not create
    duplicate records in the database.
    """
    client.force_authenticate(user=student)
    url = "/api/lesson-progress/"

    client.post(url, {"lesson": lessons[0].id, "is_completed": True})
    client.post(url, {"lesson": lessons[0].id, "is_completed": True})

    assert LessonProgress.objects.filter(
        user=student,
        lesson=lessons[0]
    ).count() == 1
