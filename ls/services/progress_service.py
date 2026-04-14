from ls.models import Enrollment, Lesson


def complete_lesson(user, lesson: Lesson):
    """complete lesson
    """
    enrollment = Enrollment.objects.get(user=user, course=lesson.course)

    total_lessons = lesson.course.lessons.count()
    completed_lessons = getattr(enrollment, "completed_lessons", 0) + 1

    enrollment.user_progress = int((completed_lessons / total_lessons) * 100)
    enrollment.save()

    return enrollment.user_progress
