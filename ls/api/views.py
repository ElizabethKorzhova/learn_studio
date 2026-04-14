"""This module provides DRF ViewSets for API LMS."""
from typing import Union, Type, List

from django.db.models import QuerySet
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.serializers import Serializer, CharField
from rest_framework.exceptions import PermissionDenied, ValidationError
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, inline_serializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from ls.models import Course, User, Lesson, Enrollment, Homework, HomeworkSubmission, Transaction
from . import serializers, permissions
from ls.models import LessonProgress
from .utils import update_course_progress
from ls.services.payment_service import confirm_payment
from ls.services.homework_service import grade_submission
from ls.services.notification_service import create_notification


class AuthViewSet(viewsets.GenericViewSet):
    """ViewSet for authentication action such as register, login and logout."""

    def get_permissions(self) -> List[Union[IsAuthenticated, AllowAny]]:
        """
        Returns the list of permission classes based on actions.

        Returns:
            List[Union[IsAuthenticated, AllowAny]]: the list of permissions
        """
        if self.action == "logout":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self) -> Type[Serializer]:
        """
        Returns the serializer based on the actions.

        Returns:
            Type[Serializer]: the serializer class
        """
        return serializers.RegisterSerializer if self.action == "register" \
            else serializers.LoginSerializer if self.action == "login" else Serializer

    @action(methods=["post"], detail=False)
    def register(self, request: Request) -> Response:
        """
        Register a new user and return JWT tokens.

        Args:
            request (Request): HTTP request with user registration data
        Returns:
            Response: API response with user data and JWT tokens or error message
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({"message": "User has been created",
                             "refresh": str(refresh),
                             "access": str(refresh.access_token)},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False)
    def login(self, request: Request) -> Response:
        """
        Login the user and return JWT tokens.

        Args:
            request (Request): HTTP request with user data
        Returns:
            Response: API response with user data and JWT tokens or error message
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"]
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({"message": "Logged in successfully",
                                 "refresh": str(refresh),
                                 "access": str(refresh.access_token),
                                 "user": serializers.UserSerializer(user).data},
                                status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=inline_serializer(
            name="LogoutRequest",
            fields={
                "refresh": CharField(help_text="Refresh token"),
            }
        ),
    )
    @action(methods=["post"], detail=False)
    def logout(self, request: Request) -> Response:
        """
        Logout user by blacklisting refresh token.

        Args:
            request (Request): HTTP request with refresh token
        Returns:
            Response: API response with success or error message
        """
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required for logout"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"},
                            status=status.HTTP_200_OK)
        except TokenError:
            return Response({"error": "Token is invalid or already blacklisted"},
                            status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """ViewSet for User management endpoint."""
    queryset = User.objects.all()

    def get_serializer_class(self) -> Type[Serializer]:
        """
        Returns the serializer class based on action

        Returns:
            Type[Serializer]: the serializer class
        """
        if self.action == "me":
            return serializers.MyProfileSerializer
        return serializers.UserSerializer

    @action(methods=["get", "patch", "delete"], detail=False)
    def me(self, request: Request) -> Response | None:
        """
        Action to manage current user profile.

        Args:
            request (Request): HTTP request
        Returns:
            Response: API response with user data or operation result
        """
        user = request.user

        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        elif request.method == "PATCH":
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == "DELETE":
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course management endpoint."""
    queryset = Course.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self) -> Type[Serializer]:
        """
        Returns the serializer class based on action

        Returns:
            Type[Serializer]: the serializer class
        """
        if self.action == "retrieve":
            return serializers.CourseDetailSerializer
        return serializers.CourseSerializer

    def get_permissions(self) -> List[Type[BasePermission]]:
        """
        Returns the list of permissions required for the action.

        Returns:
            List[Type[BasePermission]]: the list of permissions
        """
        permission_classes = [permissions.IsInstructorOrAdmin] if self.action == "create" else [
            permissions.IsOwnerOrAdmin] if self.action in ("partial_update", "destroy") else [
            permissions.IsEnrolledOrStuff] if self.action == "participants" else [
            IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer: Serializer) -> None:
        """
        Create a new course with current user as instructor.

        Args:
            serializer (Serializer): serializer object
        """
        serializer.save(instructor=self.request.user)

    @action(methods=["get"], detail=False)
    def my(self, request: Request) -> Response:
        """
        Action to manage user courses.

        Args:
            request (Request): HTTP request
        Returns:
            Response: API response with list of courses for student or instructor
        """
        user = request.user
        queryset = Course.objects.filter(enrollments__user=user) if user.role == "student" else Course.objects.filter(
            instructor=user) if user.role == "instructor" else Course.objects.none()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def participants(self, request: Request, pk: int | None = None) -> Response:
        """
        Action to get all participants of course.

        Args:
            request (Request): HTTP request
            pk (int | None): id
        Returns:
            Response: API response with list of enrolled students.
        """
        course = self.get_object()
        enrollments = Enrollment.objects.filter(course=course)
        serializer = serializers.ParticipantSerializer(enrollments, many=True)
        return Response(serializer.data)


@extend_schema_view(
    create=extend_schema(
        parameters=[
            OpenApiParameter(
                name="course_id",
                location=OpenApiParameter.QUERY,
                required=True,
                type=int,
            )
        ]
    )
)
class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet for Lesson management endpoint."""
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["course_id"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self) -> List[Type[BasePermission]]:
        """
        Returns the list of permissions based on the action.

        Returns:
            List[Type[BasePermission]]: the list of permissions
        """
        if self.action in ("create", "partial_update", "destroy"):
            return [permissions.IsOwnerOrAdmin()]
        return [permissions.IsEnrolledOrStuff()]

    def get_queryset(self) -> QuerySet[Lesson]:
        """
        Filters lessons based on course and user access.

        Returns:
            QuerySet[Lesson]: the queryset of filtered lessons
        Raises:
            PermissionDenied: if the user does not have enrolled or another instructor
        """

        if self.action in ("retrieve", "partial_update", "destroy"):
            return Lesson.objects.all()

        user = self.request.user
        course_id = self.request.query_params.get("course_id")

        if not course_id:
            return Lesson.objects.none()

        course = get_object_or_404(Course, id=course_id)
        queryset = Lesson.objects.filter(course_id=course_id)

        if user.role == "admin":
            return queryset.order_by("order_index")

        if user.role == "instructor":
            if course.instructor != user:
                raise PermissionDenied("You are not the instructor for this course")
            return queryset.filter(course__instructor=user).order_by("order_index")

        if user.role == "student":
            if not course.enrollments.filter(user=user).exists():
                raise PermissionDenied("You are not enrolled for this course")
            return queryset.filter(course__enrollments__user=user).order_by("order_index")

        raise PermissionDenied("Access denied")

    def perform_create(self, serializer: Serializer) -> None:
        """
        Creates a new lesson in the specific course.

        Args:
            serializer (Serializer): serializer object
        Raises:
            PermissionDenied: if the user is the instructor of another course
            ValidationError: if there is no course_id
        """
        user = self.request.user
        course_id = self.request.query_params.get("course_id")

        if not course_id:
            raise ValidationError("course_id is required")

        course = get_object_or_404(Course, id=course_id)
        if user.role == "instructor" and course.instructor != user:
            raise PermissionDenied("You are not the instructor for this course")
        serializer.save(course=course)


@extend_schema_view(
    create=extend_schema(
        parameters=[
            OpenApiParameter(
                name="lesson_id",
                location=OpenApiParameter.QUERY,
                required=True,
                type=int,
            )
        ]
    )
)
class HomeworkViewSet(viewsets.ModelViewSet):
    """ViewSet for Homework management endpoint."""
    queryset = Homework.objects.all()
    serializer_class = serializers.HomeworkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["lesson_id"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self) -> List[Type[BasePermission]]:
        """
        Returns the list of permissions based on the action.

        Returns:
            List[Type[BasePermission]]: the list of permissions
        """
        if self.action in ("create", "partial_update", "destroy"):
            return [(permissions.IsInstructor & permissions.IsCourseInstructor)()]
        return [permissions.IsEnrolledOrStuff()]

    def get_queryset(self) -> QuerySet[Homework]:
        """
        Filters homeworks based on lesson and user access.

        Returns:
            QuerySet[Homework]: the queryset of filtered homeworks
        Raises:
            PermissionDenied: if the user does not have enrolled or another instructor
        """
        if self.action in ("retrieve", "partial_update", "destroy"):
            return Homework.objects.all()

        user = self.request.user
        lesson_id = self.request.query_params.get("lesson_id")

        if not lesson_id:
            return Homework.objects.none()

        lesson = get_object_or_404(Lesson, id=lesson_id)
        queryset = Homework.objects.filter(lesson_id=lesson_id)

        if user.role == "admin":
            return queryset

        if user.role == "instructor":
            if lesson.course.instructor != user:
                raise PermissionDenied("You are not the instructor for this course")
            return queryset.filter(lesson__course__instructor=user)

        if user.role == "student":
            if not lesson.course.enrollments.filter(user=user).exists():
                raise PermissionDenied("You are not enrolled for this course")
            return queryset.filter(lesson__course__enrollments__user=user)

        raise PermissionDenied("Access denied")

    def perform_create(self, serializer: Serializer) -> None:
        """
        Creates a new homework in the specific lesson.

        Args:
            serializer (Serializer): serializer object
        Raises:
            PermissionDenied: if the user is the instructor of another course
            ValidationError: if there is no course_id
        """
        user = self.request.user
        lesson_id = self.request.query_params.get("lesson_id")

        if not lesson_id:
            raise ValidationError("lesson_id is required")

        lesson = get_object_or_404(Lesson, id=lesson_id)
        if user.role == "instructor" and lesson.course.instructor != user:
            raise PermissionDenied("You are not the instructor for this course")
        serializer.save(lesson=lesson, created_by=user)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Enrollment management endpoint."""
    queryset = Enrollment.objects.all()
    serializer_class = serializers.EnrollmentSerializer
    http_method_names = ["get", "post", "delete"]

    def get_permissions(self) -> List[BasePermission]:
        """
        Returns the list of permissions based on the action.

        Returns:
            List[BasePermission]: the list of permissions
        """
        if self.action == "create":
            return [permissions.IsStudent()]
        elif self.action == "destroy":
            return [(permissions.IsStudent & permissions.IsEnrolledStudent)()]
        return [permissions.IsEnrolledOrStuff()]

    def get_queryset(self) -> QuerySet[Enrollment]:
        """
        Filters enrollments based on course and user access.

        Returns:
            QuerySet[Enrollment]: the queryset of filtered enrollments
        """
        user = self.request.user
        queryset = self.queryset.select_related("course", "user")

        if user.role == "admin":
            return queryset
        if user.role == "instructor":
            return queryset.filter(course__instructor=user)
        if user.role == "student":
            return queryset.filter(user=user)
        return queryset.none()

    def perform_create(self, serializer: Serializer) -> None:
        """
        Creates a new enrollment for authenticated student.

        Args:
            serializer (Serializer): serializer object
        Raises:
            PermissionDenied: if the user is not a student
            ValidationError: if the student have already enrolled
        """
        user = self.request.user
        course = serializer.validated_data.get("course")

        if user.role != "student":
            raise PermissionDenied("Only students can enroll")
        if Enrollment.objects.filter(user=user, course=course).exists():
            raise ValidationError("You are already enrolled")

        serializer.save(user=user)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="homework_id",
                location=OpenApiParameter.QUERY,
                required=True,
                type=int,
            ),
        ]
    ),
    create=extend_schema(
        parameters=[
            OpenApiParameter(
                name="homework_id",
                location=OpenApiParameter.QUERY,
                required=True,
                type=int,
            )
        ]
    )
)
class HomeworkSubmissionViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet
                                ):
    """ViewSet for HomeworkSubmission management endpoint."""
    queryset = HomeworkSubmission.objects.all()

    def get_serializer_class(self) -> Type[Serializer]:
        """
        Returns the serializer class based on the action.

        Returns:
            Type[Serializer]: the serializer class
        """
        if self.action == "create":
            return serializers.SubmissionCreateSerializer
        if self.action == "grade":
            return serializers.GradeSerializer
        if self.action == "messages":
            return serializers.MessageSerializer
        return serializers.SubmissionSerializer

    def get_permissions(self) -> List[BasePermission]:
        """
        Returns the list of permissions based on the action.

        Returns:
            List[BasePermission]: the list of permissions
        """
        if self.action == "create":
            return [(permissions.IsStudent & permissions.IsEnrolledStudent)()]
        elif self.action == "grade":
            return [(permissions.IsInstructor & permissions.IsCourseInstructor)()]
        return [permissions.IsEnrolledOrStuff()]

    def get_queryset(self) -> QuerySet[HomeworkSubmission]:
        """
        Filters homework submissions based on homework and user access.

        Returns:
            QuerySet[HomeworkSubmission]: the queryset of filtered homework submissions
        """
        queryset = super().get_queryset()
        homework_id = self.request.query_params.get("homework_id")

        if homework_id:
            queryset = queryset.filter(homework_id=homework_id)

        user = self.request.user
        if user.role == "student":
            return queryset.filter(user=user)
        if user.role == "instructor":
            return queryset.filter(homework__lesson__course__instructor=user)
        return queryset

    def perform_create(self, serializer: Serializer) -> None:
        """
        Creates a new enrollment for the student.

        Args:
            serializer (Serializer): serializer object
        Raises:
            PermissionDenied: if the user is not a student or is not enrolled student
            ValidationError: if there are no homework_id
        """
        user = self.request.user
        homework_id = self.request.query_params.get("homework_id")

        if not homework_id:
            raise ValidationError("homework_id is required")

        homework = get_object_or_404(Homework, id=homework_id)

        if user.role == "instructor" or user.role == "admin":
            raise PermissionDenied("You cannot submit homework")

        if not homework.lesson.course.enrollments.filter(user=user).exists():
            raise PermissionDenied("You are not enrolled for this course")

        serializer.save(user=user, homework=homework)

    @action(detail=True, methods=["patch"])
    def grade(self, request, pk=None):
        submission = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        grade_submission(
            submission,
            serializer.validated_data["score"]
        )

        return Response({"message": "Successfully graded"})

    @action(detail=True, methods=["get", "post"])
    def messages(self, request: Request, pk: int | None = None) -> Response | None:
        """
        Action to manage messages.

        Args:
            request (Request): the request object
            pk (int | None): id
        Returns:
            Response: API response with list of messages or created message
        """

        submission = self.get_object()

        if request.method == "GET":
            messages = submission.messages.all().order_by("created_at")
            serializer = serializers.MessageSerializer(messages, many=True)
            return Response(serializer.data)

        serializer = serializers.MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.save(
            sender=request.user,
            homework_submission=submission
        )

        create_notification(
            user=submission.user,
            message="New message on your homework",
            type_="message"
        )

        return Response(serializers.MessageSerializer(message).data)


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for Transaction management endpoint
    """
    queryset = Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """The user can only see their own transactions
        """
        return Transaction.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Returns the appropriate serializer class based on the current action
        """
        if self.action == "confirm":
            return serializers.TransactionConfirmSerializer
        return serializers.TransactionSerializer

    def perform_create(self, serializer):
        """Creates a new transaction for the authenticated user
        """

        course = serializer.validated_data["course"]

        serializer.save(
            user=self.request.user,
            amount=course.price,
            status="pending"
        )

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        transaction = get_object_or_404(Transaction, pk=pk)

        if transaction.user != request.user:
            raise PermissionDenied("Not your transaction")

        confirm_payment(transaction)  # 👈 ТУТ SERVICE

        return Response({"message": "Payment successful"})


class LessonProgressViewSet(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """Lesson progress viewset
    """
    serializer_class = serializers.LessonProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return a list of all lesson progress records for the currently authenticated user.
        """
        return LessonProgress.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new progress record or update an existing one for a specific lesson.

        Logic:
        - Validates input data.
        - Uses 'update_or_create' to ensure a unique record per user-lesson pair.
        - Sets 'completed_at' timestamp if the lesson is marked as completed.
        - Triggers an overall course progress recalculation
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lesson = serializer.validated_data['lesson']
        is_completed = serializer.validated_data.get('is_completed', True)

        progress, created = LessonProgress.objects.update_or_create(
            user=self.request.user,
            lesson=lesson,
            defaults={'is_completed': is_completed}
        )

        if progress.is_completed and not progress.completed_at:
            from django.utils.timezone import now
            progress.completed_at = now()
            progress.save()

        update_course_progress(self.request.user, lesson.course)

        output_serializer = self.get_serializer(progress)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(output_serializer.data, status=status_code)

    def perform_update(self, serializer):
        """Update an existing lesson progress record.

        If the status changes to 'completed', the 'completed_at' timestamp is set,
        and the total course progress is recalculated.
        """
        progress = serializer.save()

        if progress.is_completed and not progress.completed_at:
            from django.utils.timezone import now
            progress.completed_at = now()
            progress.save()

        update_course_progress(self.request.user, progress.lesson.course)


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for user notifications
    """

    serializer_class = serializers.NotificationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        """User can see only own notifications
        """
        return self.request.user.notifications.all()

    @action(detail=False, methods=["patch"])
    def mark_all_as_read(self, request):
        """Mark all notifications as read
        """
        updated = request.user.notifications.filter(is_read=False).update(is_read=True)
        return Response({"marked_as_read": updated})

    @action(detail=True, methods=["patch"])
    def mark_as_read(self, request, pk=None):
        """Mark single notification as read
        """
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read"})
