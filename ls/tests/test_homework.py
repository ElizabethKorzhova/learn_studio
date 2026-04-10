import pytest
from rest_framework import status

from ls.models import Homework, Enrollment


@pytest.fixture
def homework(lesson, instructor_user):
    return Homework.objects.create(
        lesson=lesson,
        title="HW 1",
        task="Solve exercises",
        deadline="2026-01-10T10:00:00Z",
        complexity=2,
        deadline_date="2026-01-10",
        created_by=instructor_user
    )


@pytest.mark.django_db
def test_instructor_can_create_homework(api_client, instructor_user, lesson):
    """ Test that an instructor can create a homework
    """
    api_client.force_authenticate(user=instructor_user)

    res = api_client.post(
        f"/api/homeworks/?lesson_id={lesson.id}",
        {
            "title": "HW 1",
            "task": "Solve tasks",
            "deadline": "2026-01-10T10:00:00Z",
            "complexity": 3,
            "deadline_date": "2026-01-10"
        },
        format="json"
    )

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["title"] == "HW 1"


# ⇓⇓⇓⇓ цей тест ми не пройшли!!!! Студент може створити домашку !!!!
@pytest.mark.django_db
def test_student_cannot_create_homework(api_client, student_user, lesson):
    """ Test that a student can not create a homework
    """
    api_client.force_authenticate(user=student_user)

    res = api_client.post(
        f"/api/homeworks/?lesson_id={lesson.id}",
        {
            "title": "Hack HW",
            "task": "bad attempt",
            "deadline": "2026-01-10T10:00:00Z",
            "complexity": 1,
            "deadline_date": "2026-01-10"
        },
        format="json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_enrolled_user_can_list_homeworks(
        api_client, student_user, course, lesson, homework
):
    """ Test that a user who enrolled can list homeworks
    """
    Enrollment.objects.create(
        user=student_user,
        course=course,
        course_status="active",
        user_progress=10,
        attendance=100
    )

    api_client.force_authenticate(user=student_user)

    res = api_client.get(f"/api/homeworks/?lesson_id={lesson.id}")

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) >= 1
    assert res.data[0]["title"] == homework.title


@pytest.mark.django_db
def test_not_enrolled_user_cannot_list_homeworks(api_client, student_user, lesson):
    """Test that a user cannot list homeworks when they are not enrolled
    """
    api_client.force_authenticate(user=student_user)

    res = api_client.get(f"/api/homeworks/?lesson_id={lesson.id}")

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_instructor_can_list_homeworks(
        api_client, instructor_user, lesson, homework
):
    """ Test that instructor can list all homeworks
    """
    api_client.force_authenticate(user=instructor_user)

    res = api_client.get(f"/api/homeworks/?lesson_id={lesson.id}")

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) >= 1


@pytest.mark.django_db
def test_retrieve_homework(api_client, student_user, course, lesson, homework):
    """ Test that a homework can be retrieved
    """

    Enrollment.objects.create(
        user=student_user,
        course=course,
        course_status="active",
        user_progress=0,
        attendance=0
    )

    api_client.force_authenticate(user=student_user)

    res = api_client.get(f"/api/homeworks/{homework.id}/")

    assert res.status_code == status.HTTP_200_OK
    assert res.data["title"] == homework.title


@pytest.mark.django_db
def test_student_cannot_update_homework(api_client, student_user, homework):
    """ Test that a student can not  update  homework
    """
    api_client.force_authenticate(user=student_user)

    res = api_client.patch(
        f"/api/homeworks/{homework.id}/",
        {"title": "Hacked HW"},
        format="json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_instructor_can_update_homework(api_client, instructor_user, homework):
    """ Test that instructor can update a homework
    """
    api_client.force_authenticate(user=instructor_user)

    res = api_client.patch(
        f"/api/homeworks/{homework.id}/",
        {"title": "Updated HW"},
        format="json"
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["title"] == "Updated HW"


@pytest.mark.django_db
def test_instructor_can_delete_homework(api_client, instructor_user, homework):
    """ test that an instructor can delete a homework
    """
    api_client.force_authenticate(user=instructor_user)

    res = api_client.delete(f"/api/homeworks/{homework.id}/")

    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert not Homework.objects.filter(id=homework.id).exists()
