from rest_framework import permissions

from ls.models import Enrollment
from .utils import get_course_from_obj


class BaseRolePermission(permissions.BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and request.user.role in self.allowed_roles
        )


class IsAdmin(BaseRolePermission):
    allowed_roles = ["admin"]


class IsInstructor(BaseRolePermission):
    allowed_roles = ["instructor"]


class IsStudent(BaseRolePermission):
    allowed_roles = ["student"]


class IsCourseInstructor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        course = get_course_from_obj(obj)
        return course and course.instructor == request.user


class IsEnrolledStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Enrollment):
            return obj.user == request.user
        course = get_course_from_obj(obj)
        return course and course.enrollments.filter(user=request.user).exists()


IsInstructorOrAdmin = IsInstructor | IsAdmin
IsOwnerOrAdmin = (IsInstructor & IsCourseInstructor) | IsAdmin
IsEnrolledOrStuff = (IsStudent & IsEnrolledStudent) | IsOwnerOrAdmin
