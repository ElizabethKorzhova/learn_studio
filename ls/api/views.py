from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.serializers import Serializer, CharField
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, inline_serializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from ls.models import Course, User, Lesson, Enrollment, Homework
from . import serializers
from . import permissions


class AuthViewSet(viewsets.GenericViewSet):
    def get_permissions(self):
        if self.action == "logout":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        return serializers.RegisterSerializer if self.action == "register" \
            else serializers.LoginSerializer if self.action == "login" else Serializer

    @action(methods=["post"], detail=False)
    def register(self, request):
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
    def login(self, request):
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
    def logout(self, request):
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
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "me":
            return serializers.MyProfileSerializer
        return serializers.UserSerializer

    @action(methods=["get", "patch", "delete"], detail=False)
    def me(self, request):
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
    queryset = Course.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CourseDetailSerializer
        return serializers.CourseSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsInstructorOrAdmin] if self.action == "create" else [
            permissions.IsOwnerOrAdmin] if self.action in ("partial_update", "destroy") else [
            permissions.IsEnrolledOrStuff] if self.action == "participants" else [
            IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    @action(methods=["get"], detail=False)
    def my(self, request):
        user = request.user
        queryset = Course.objects.filter(enrollments__user=user) if user.role == "student" else Course.objects.filter(
            instructor=user) if user.role == "instructor" else Course.objects.none()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def participants(self, request, pk=None):
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
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["course_id"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        if self.action in ("create", "partial_update", "destroy"):
            return [permissions.IsOwnerOrAdmin()]
        return [permissions.IsEnrolledOrStuff()]

    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")
        if self.action == "list":
            return self.queryset.filter(course_id=course_id).order_by("order_index")
        return self.queryset

    def perform_create(self, serializer):
        course_id = self.request.query_params.get("course_id")
        course = get_object_or_404(Course, id=course_id)
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
    queryset = Homework.objects.all()
    serializer_class = serializers.HomeworkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["lesson_id"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        if self.action in ("create", "partial_update", "destroy"):
            return [permissions.CanManageHomework()]
        return [permissions.IsEnrolledOrStuff()]

    def get_queryset(self):
        lesson_id = self.request.query_params.get("lesson_id")
        if self.action == "list":
            return self.queryset.filter(lesson_id=lesson_id)
        return self.queryset

    def perform_create(self, serializer):
        lesson_id = self.request.query_params.get("lesson_id")
        lesson = get_object_or_404(Lesson, id=lesson_id)
        serializer.save(lesson=lesson, created_by=self.request.user)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = serializers.EnrollmentSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.select_related("course", "user")
        return queryset.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data.get("course")

        if not Enrollment.objects.filter(user=user, course=course).exists() or not course.instructor == user:
            serializer.save(user=user)
