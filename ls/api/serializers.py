"""This module provides DRF serializers for LMS."""
from typing import Dict, Any

from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from ls import models


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for register user."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ["email", "username", "password", "first_name", "last_name", "role"]

    def create(self, validated_data: Dict[str, Any]) -> models.User:
        """
        Create a new user with hashed password.

        Args:
            validated_data (Dict[str, Any]): data used to create a new user
        Returns:
            models.User: Created user
        """
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    """Serializer for login user."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class SocialLinkSerializer(serializers.ModelSerializer):
    """Serializer for social links."""

    class Meta:
        model = models.SocialLink
        fields = ["platform_name", "url"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user."""
    social_links = SocialLinkSerializer(many=True, read_only=True)

    class Meta:
        model = models.User
        fields = ["id", "username", "email", "first_name", "last_name", "social_links"]
        read_only_fields = fields


class UserShortSerializer(serializers.ModelSerializer):
    """Serializer for user in a short form."""

    class Meta:
        model = models.User
        fields = ["id", "first_name", "last_name"]
        read_only_fields = fields


class MyProfileSerializer(serializers.ModelSerializer):
    """Serializer for profile data."""
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = models.User
        fields = ["id", "username", "email", "first_name", "last_name", "social_links"]
        read_only_fields = ["id", "role"]


class LessonShortSerializer(serializers.ModelSerializer):
    """Serializer for lesson in a short form."""

    class Meta:
        model = models.Lesson
        fields = ["id", "title", "order_index"]


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for lesson."""

    class Meta:
        model = models.Lesson
        fields = ["id", "title", "content", "order_index", "images"]
        read_only_fields = ["id"]


class HomeworkSerializer(serializers.ModelSerializer):
    """Serializer for homework."""
    created_by = UserShortSerializer(read_only=True)

    class Meta:
        model = models.Homework
        fields = ["id", "title", "task", "deadline", "complexity", "deadline_date", "created_by"]
        read_only_fields = ["id", "created_by"]


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for course."""
    instructor = UserSerializer(read_only=True)
    is_enrolled = serializers.SerializerMethodField()
    user_stats = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = [
            "id", "is_enrolled", "title", "description", "price",
            "start_at", "duration", "created_at", 'user_stats', "instructor", "progress"
        ]
        read_only_fields = ["id", "created_at"]

    def get_is_enrolled(self, obj):
        request = self.context.get("request")
        return models.Enrollment.objects.filter(user=request.user, course=obj).exists()

    def get_user_stats(self, obj):
        request = self.context.get("request")
        last_enrollment = models.Enrollment.objects.filter(user=request.user, course=obj).last()
        if last_enrollment:
            return EnrollmentSerializer(last_enrollment, many=False, read_only=True).data
        return None

    def get_progress(self, obj):
        request = self.context.get("request")

        enrollment = models.Enrollment.objects.filter(
            user=request.user,
            course=obj
        ).first()

        return enrollment.user_progress if enrollment else 0


class CourseDetailSerializer(CourseSerializer):
    """Serializer for course with lessons."""
    lessons = LessonShortSerializer(many=True, read_only=True)

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ["lessons"]


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for enrollment."""
    course_title = serializers.CharField(source="course.title", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = models.Enrollment
        fields = ["id", "user", "course", "course_title", "user_email", "enrolled_at", "user_progress",
                  "attendance", "updated_at"]
        read_only_fields = ["id", "user", "user_progress", "attendance", "enrolled_at", "updated_at"]


class ParticipantSerializer(serializers.ModelSerializer):
    """Serializer for participant of the course."""
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = models.Enrollment
        fields = ["user"]


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transaction"""

    user = UserShortSerializer(read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)

    payment_data = serializers.JSONField(required=False, default=dict)

    class Meta:
        model = models.Transaction
        fields = [
            "id",
            "user",
            "course",
            "course_title",
            "amount",
            "status",
            "payment_data",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "amount",
            "status",
            "created_at",
        ]

    def validate(self, attrs):
        """Validates that the user has not already successfully purchased the course
        Args:
        attrs (dict): Incoming validated data from the serializer

        Returns:
        dict: The validated attributes if validation passes

        Raises:
        serializers.ValidationError: If the user has already purchased the course
        """
        user = self.context["request"].user
        course = attrs.get("course")

        if models.Transaction.objects.filter(
                user=user,
                course=course,
                status="success"
        ).exists():
            raise serializers.ValidationError(
                "You already purchased this course"
            )

        return attrs


class TransactionConfirmSerializer(serializers.Serializer):
    """Serializer for transaction confirmation
    """
    payment_data = serializers.JSONField()


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for message."""
    sender = UserShortSerializer(read_only=True)

    class Meta:
        model = models.Message
        fields = "__all__"
        read_only_fields = ["homework_submission", "sender", "created_at"]


class SubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating submission."""
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = models.HomeworkSubmission
        fields = ["id", "homework", "user", "files", "url"]
        read_only_fields = ["id", "homework"]


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializer for submission."""
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = models.HomeworkSubmission
        fields = "__all__"
        read_only_fields = ["user", "score", "submitted_at"]


class GradeSerializer(serializers.Serializer):
    """Serializer for grading submission."""
    score = serializers.IntegerField(min_value=0, max_value=100)


class LessonProgressSerializer(serializers.ModelSerializer):
    """Serializer for lesson progress.
    """

    class Meta:
        model = models.LessonProgress
        fields = ["id", "lesson", "is_completed", "completed_at"]
        read_only_fields = ["id", "completed_at"]
