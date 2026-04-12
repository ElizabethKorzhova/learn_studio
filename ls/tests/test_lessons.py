import pytest
from rest_framework import status

from ls.models import Lesson, Enrollment


@pytest.fixture
def lesson(course):
    return Lesson.objects.create(
        course=course,
        title="Algebra 1",
        content="Intro to algebra",
        order_index=1
    )


@pytest.mark.django_db
def test_instructor_can_create_lesson(api_client, instructor_user, course):
    """Test that the instructor can create a lesson.
    """
    api_client.force_authenticate(user=instructor_user)

    res = api_client.post(
        f"/api/lessons/?course_id={course.id}",
        {
            "title": "Lesson 1",
            "content": "Intro to algebra",
            "order_index": 1
        },
        format="json"
    )

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["title"] == "Lesson 1"


@pytest.mark.django_db
def test_student_cannot_create_lesson(api_client, student_user, course):
    """Test that the student can not create a lesson
    """
    api_client.force_authenticate(user=student_user)

    res = api_client.post(
        f"/api/lessons/?course_id={course.id}",
        {
            "title": "Hack Lesson",
            "content": "Should fail",
            "order_index": 1
        },
        format="json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_enrolled_user_can_list_lessons(
        api_client, student_user, course, lesson
):
    """Test that the enrolled user can list lessons
    """
    Enrollment.objects.create(
        user=student_user,
        course=course,
        course_status="active",
        user_progress=0,
        attendance=0
    )

    api_client.force_authenticate(user=student_user)

    res = api_client.get(f"/api/lessons/?course_id={course.id}")

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) >= 1
    assert res.data[0]["title"] == lesson.title


@pytest.mark.django_db
def test_not_enrolled_user_cannot_list_lessons(api_client, student_user, course):
    """Test that not enrolled users cannot list lessons
    """
    api_client.force_authenticate(user=student_user)

    res = api_client.get(f"/api/lessons/?course_id={course.id}")

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_instructor_can_list_own_course_lessons(
        api_client, instructor_user, course, lesson
):
    """Test that the instructor can list own course lessons
    """
    api_client.force_authenticate(user=instructor_user)

    res = api_client.get(f"/api/lessons/?course_id={course.id}")

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) >= 1


@pytest.mark.django_db
def test_retrieve_lesson(api_client, student_user, course, lesson):
    """Test that the lesson can be retrieved
    """
    Enrollment.objects.create(
        user=student_user,
        course=course,
        course_status="active",
        user_progress=0,
        attendance=0
    )

    api_client.force_authenticate(user=student_user)

    res = api_client.get(f"/api/lessons/{lesson.id}/")

    assert res.status_code == status.HTTP_200_OK
    assert res.data["title"] == lesson.title


@pytest.mark.django_db
def test_student_cannot_update_lesson(api_client, student_user, lesson):
    """Test that the student cannot update lesson
    """
    api_client.force_authenticate(user=student_user)

    res = api_client.patch(
        f"/api/lessons/{lesson.id}/",
        {"title": "Hacked"},
        format="json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_instructor_can_update_lesson(api_client, instructor_user, lesson):
    """Test that the instructor can update lesson
    """
    api_client.force_authenticate(user=instructor_user)

    res = api_client.patch(
        f"/api/lessons/{lesson.id}/",
        {"title": "Updated lesson"},
        format="json"
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["title"] == "Updated lesson"


@pytest.mark.django_db
def test_instructor_can_delete_lesson(api_client, instructor_user, lesson):
    """Test that the instructor can delete lesson
    """
    api_client.force_authenticate(user=instructor_user)

    res = api_client.delete(f"/api/lessons/{lesson.id}/")

    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert not Lesson.objects.filter(id=lesson.id).exists()
# тести пройдені