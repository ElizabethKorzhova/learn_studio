import pytest
from rest_framework import status


@pytest.mark.django_db
def test_create_course_as_instructor(api_client, instructor_user):
    """ Test that instructor can create a new course
    """
    api_client.force_authenticate(user=instructor_user)

    res = api_client.post("/api/courses/", {
        "title": "Physics",
        "description": "Test course",
        "price": "50.00",
        "start_at": "2026-01-01T10:00:00Z",
        "duration": 10
    }, format="json")

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["title"] == "Physics"


@pytest.mark.django_db
def test_student_cannot_create_course(api_client, student_user):
    """ Test that student can not create a new course
    """
    api_client.force_authenticate(user=student_user)

    res = api_client.post("/api/courses/", {
        "title": "Physics",
        "description": "Test course",
        "price": "50.00",
        "start_at": "2026-01-01T10:00:00Z",
        "duration": 10
    }, format="json")

    assert res.status_code == status.HTTP_403_FORBIDDEN

#⇓⇓⇓⇓ цей тест ми не пройшли !!! Не авторизований користувач може створювати курс !!!!!
@pytest.mark.django_db
def test_unauthenticated_cannot_create_course(api_client):
    """ Test that Guest can not create a new course
    """
    res = api_client.post("/api/courses/", {
        "title": "Physics",
        "description": "Test course",
        "price": "50.00",
        "start_at": "2026-01-01T10:00:00Z",
        "duration": 10
    }, format="json")

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_list_courses_authenticated(api_client, instructor_user, course):
    """ Test that autorizated users  can list courses
    """
    api_client.force_authenticate(user=instructor_user)

    res = api_client.get("/api/courses/")

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) >= 1


@pytest.mark.django_db
def test_retrieve_course(api_client, instructor_user, course):
    """ Test retrieving a course
    """
    api_client.force_authenticate(user=instructor_user)

    res = api_client.get(f"/api/courses/{course.id}/")

    assert res.status_code == status.HTTP_200_OK
    assert res.data["title"] == course.title


@pytest.mark.django_db
def test_student_cannot_update_course(api_client, student_user, course):
    """ Test that student cannot update a course
    """
    api_client.force_authenticate(user=student_user)

    res = api_client.patch(f"/api/courses/{course.id}/", {
        "title": "Hacked title"
    }, format="json")

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_instructor_can_update_own_course(api_client, instructor_user, course):
    """ Test that instructor can update own course
    """
    api_client.force_authenticate(user=instructor_user)

    res = api_client.patch(f"/api/courses/{course.id}/", {
        "title": "Updated title"
    }, format="json")

    assert res.status_code == status.HTTP_200_OK
    assert res.data["title"] == "Updated title"
