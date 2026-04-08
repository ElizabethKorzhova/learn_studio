from rest_framework import permissions

from ls.models import Enrollment, Course
from ls.models import Lesson, Homework


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == "admin"


class IsInstructor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == "instructor"


class IsStudent(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == "student"


class IsInstructorOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "admin" or request.user.role == "instructor"


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "admin": return True
        if view.action == "create":
            homework_id = request.query_params.get("homework_id")
            if homework_id:
                homework = Homework.objects.filter(id=homework_id).select_related("lesson").first()
                if homework:
                    return Enrollment.objects.filter(
                        user=request.user,
                        course_id=homework.lesson.course_id
                    ).exists()
            course_id = request.query_params.get("course_id")
            if course_id: return Course.objects.filter(id=course_id, instructor=request.user).exists()
            lesson_id = request.query_params.get("lesson_id")
            if lesson_id: return Lesson.objects.filter(id=lesson_id, course__instructor=request.user).exists()
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == "admin": return True
        if hasattr(obj, "student"):
            return obj.student == user or obj.homework.lesson.course.instructor == user
        if hasattr(obj, "instructor"): return obj.instructor == user
        if hasattr(obj, "course"): return obj.course.instructor == user
        if hasattr(obj, "lesson"): return obj.lesson.course.instructor == user
        return False


class CanManageHomework(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "lesson"):
            instructor = obj.lesson.course.instructor
        elif hasattr(obj, "homework"):
            instructor = obj.homework.lesson.course.instructor
        else:
            return False
        return instructor == request.user


class IsEnrolledOrStuff(permissions.BasePermission):

    @staticmethod
    def _check_access(user, course_id):
        if user.role == "admin": return True
        is_instructor = Course.objects.filter(id=course_id, instructor=user).exists()
        is_student = Enrollment.objects.filter(user=user, course_id=course_id).exists()
        return is_instructor or is_student

    def has_permission(self, request, view):
        if not request.user.is_authenticated: return False
        if view.detail: return True
        course_id = request.query_params.get("course_id")
        if not course_id:
            lesson_id = request.query_params.get("lesson_id")
            if lesson_id:
                lesson = Lesson.objects.filter(id=lesson_id).only("course_id").first()
                if lesson: course_id = lesson.course_id

            homework_id = request.query_params.get("homework_id")
            if homework_id:
                hw = Homework.objects.filter(id=homework_id).select_related("lesson").first()
                if hw: course_id = hw.lesson.course_id
        if not course_id: return False
        return self._check_access(request.user, course_id)

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "homework"):
            if request.user.role == "student" and obj.student != request.user:
                return False
            return self._check_access(request.user, obj.homework.lesson.course_id)
        if hasattr(obj, "instructor"): return self._check_access(request.user, obj.id)
        if hasattr(obj, "course_id"): return self._check_access(request.user, obj.course_id)
        if hasattr(obj, "lesson"): return self._check_access(request.user, obj.lesson.course_id)
        return False
