"""This module provides helper functions for LMS."""
from typing import Union

from ls.models import Course, Lesson, Homework, HomeworkSubmission, Enrollment, LessonProgress


def get_course_from_obj(
        obj: Union[Course, Lesson, Homework, HomeworkSubmission, Enrollment]
) -> Course | None:
    """
    Finds from the given object the Course and returns it.

    Args:
        obj (Union[Course, Lesson, Homework, HomeworkSubmission, Enrollment]):
         the model object related to the Course.
    Returns:
        Course: the Course or None if it was not found.
    """
    if isinstance(obj, Course):
        return obj
    if isinstance(obj, Lesson) or isinstance(obj, Enrollment):
        return obj.course
    if isinstance(obj, Homework):
        return obj.lesson.course
    if isinstance(obj, HomeworkSubmission):
        return obj.homework.lesson.course
    return None


def update_course_progress(user, course):
    """Updates the progress of a course
        """
    total_lessons = course.lessons.count()

    if total_lessons == 0:
        return 0

    completed_lessons = LessonProgress.objects.filter(
        user=user,
        lesson__course=course,
        is_completed=True
    ).count()

    progress = int((completed_lessons / total_lessons) * 100)

    Enrollment.objects.filter(user=user, course=course).update(
        user_progress=progress
    )

    return progress
