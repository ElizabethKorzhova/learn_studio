"""This module provides custom role-based DRF permissions for LMS."""
from typing import List, Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View

from ls.models import Enrollment
from .utils import get_course_from_obj


class BaseRolePermission(permissions.BasePermission):
    """
    Base permission class for role-based permissions.

    Attributes:
        allowed_roles (list[str]): list of allowed roles
    """
    allowed_roles: List[str] = []

    def has_permission(self, request: Request, view: View) -> bool:
        """
        Checks if the user is authenticated and has one of the allowed roles.

        Args:
            request (Request): request object
            view (View): view object
        Returns:
            bool: True if user is authenticated and given role is allowed otherwise False
        """
        return (
                request.user.is_authenticated
                and request.user.role in self.allowed_roles
        )


class IsAdmin(BaseRolePermission):
    """Permission class to check if user is the administrator."""
    allowed_roles = ["admin"]


class IsInstructor(BaseRolePermission):
    """Permission class to check if user is the instructor."""
    allowed_roles = ["instructor"]


class IsStudent(BaseRolePermission):
    """Permission class to check if user is the student."""
    allowed_roles = ["student"]


class IsCourseInstructor(permissions.BasePermission):
    """Permission class to check if user is the instructor of the specific course."""

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        """
        Checks if the user is the instructor or student of the specific course.

        Args:
            request (Request): request object
            view (View): view object
            obj (Any): object to be checked
        Returns:
            bool: True if user is the instructor of the specific course otherwise False
        """
        course = get_course_from_obj(obj)
        return course and course.instructor == request.user


class IsEnrolledStudent(permissions.BasePermission):
    """Permission class to check if user is the student of the specific course."""

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        """
        Checks if the user is the student of the specific course.

        Args:
            request (Request): request object
            view (View): view object
            obj (Any): object to be checked
        Returns:
            bool: True if user is the student of the specific course otherwise False
        """
        if hasattr(obj, "user") and obj.user == request.user:
            return True

        if isinstance(obj, Enrollment):
            return obj.user == request.user

        course = get_course_from_obj(obj)
        return course and course.enrollments.filter(user=request.user).exists()


IsInstructorOrAdmin = IsInstructor | IsAdmin
IsOwnerOrAdmin = (IsInstructor & IsCourseInstructor) | IsAdmin
IsEnrolledOrStuff = (IsStudent & IsEnrolledStudent) | IsOwnerOrAdmin
