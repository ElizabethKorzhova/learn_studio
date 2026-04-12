import pytest
from rest_framework import status
from django.urls import reverse

from ls.models import HomeworkSubmission, Message


@pytest.fixture
def submission(homework, student_user):
    return HomeworkSubmission.objects.create(
        homework=homework,
        user=student_user,
        url="https://test.com"
    )


@pytest.mark.django_db
def test_create_submission_success(api_client, student_user, homework, enrollment):
    """Student creates a submission successfully
    """
    api_client.force_authenticate(user=student_user)

    url = reverse("homeworksubmission-list") + f"?homework_id={homework.id}"

    response = api_client.post(url, {"url": "https://solution.com"})

    assert response.status_code == status.HTTP_201_CREATED
    assert HomeworkSubmission.objects.count() == 1


@pytest.mark.django_db
def test_create_submission_without_enrollment(api_client, student_user, homework):
    """Student creates a submission without enrollment
    """
    api_client.force_authenticate(user=student_user)

    url = reverse("homeworksubmission-list") + f"?homework_id={homework.id}"

    response = api_client.post(url, {"url": "https://fail.com"})

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_instructor_cannot_submit(api_client, instructor_user, homework):
    """Instructor attempts to submit homework
    """
    api_client.force_authenticate(user=instructor_user)

    url = reverse("homeworksubmission-list") + f"?homework_id={homework.id}"

    response = api_client.post(url, {"url": "https://fail.com"})

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_student_sees_only_own_submissions(api_client, student_user, submission):
    """Student sees only own submissions
    """
    api_client.force_authenticate(user=student_user)

    url = reverse("homeworksubmission-list") + f"?homework_id={submission.homework.id}"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_instructor_sees_course_submissions(api_client, instructor_user, submission):
    """Instructor sees course submissions
    """
    api_client.force_authenticate(user=instructor_user)

    url = reverse("homeworksubmission-list") + f"?homework_id={submission.homework.id}"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_retrieve_submission(api_client, student_user, submission):
    """Retrieve a single submission by ID
    """
    api_client.force_authenticate(user=student_user)

    url = reverse("homeworksubmission-detail", args=[submission.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == submission.id


@pytest.mark.django_db
def test_instructor_can_grade(api_client, instructor_user, submission):
    """Instructor assigns a score to a submission
    """
    api_client.force_authenticate(user=instructor_user)

    url = reverse("homeworksubmission-grade", args=[submission.id])
    response = api_client.patch(url, {"score": 90})

    submission.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert submission.score == 90


@pytest.mark.django_db
def test_student_cannot_grade(api_client, student_user, submission):
    """Student attempts to grade a submission
    """
    api_client.force_authenticate(user=student_user)

    url = reverse("homeworksubmission-grade", args=[submission.id])
    response = api_client.patch(url, {"score": 50})

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_messages(api_client, student_user, submission):
    """Retrieve messages related to a submission
    """
    Message.objects.create(
        homework_submission=submission,
        sender=student_user,
        message_text="Hello"
    )

    api_client.force_authenticate(user=student_user)

    url = reverse("homeworksubmission-messages", args=[submission.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_send_message(api_client, student_user, submission):
    """Student sends a message
    """
    api_client.force_authenticate(user=student_user)

    url = reverse("homeworksubmission-messages", args=[submission.id])
    response = api_client.post(url, {"message_text": "New message"})

    assert response.status_code == status.HTTP_200_OK
    assert Message.objects.count() == 1


@pytest.mark.django_db
def test_instructor_can_send_message(api_client, instructor_user, submission):
    """Instructor sends a message
    """
    api_client.force_authenticate(user=instructor_user)

    url = reverse("homeworksubmission-messages", args=[submission.id])
    response = api_client.post(url, {"message_text": "Feedback"})

    assert response.status_code == status.HTTP_200_OK
