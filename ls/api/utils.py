from ls.models import Course, Lesson, Homework, HomeworkSubmission, Enrollment


def get_course_from_obj(obj):
    if isinstance(obj, Course):
        return obj
    elif isinstance(obj, Lesson) or isinstance(obj, Enrollment):
        return obj.course
    elif isinstance(obj, Homework):
        return obj.lesson.course
    elif isinstance(obj, HomeworkSubmission):
        return obj.homework.lesson.course
    return None
