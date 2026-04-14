import pytest
from ls.models import HomeworkSubmission
from ls.services.homework_service import grade_submission


@pytest.mark.django_db
def test_grade_submission_updates_score(submission_factory):
    """test grade submission updates
    """
    submission = submission_factory(score=None)

    grade_submission(submission, 85)

    submission.refresh_from_db()

    assert submission.score == 85
