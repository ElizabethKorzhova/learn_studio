from ls.models import HomeworkSubmission


def grade_submission(submission: HomeworkSubmission, score: int):
    """Grade submission
    """
    submission.score = score
    submission.save()

    return submission
