"""This module provides URL configuration for the API."""
from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()
router.register(r"auth", views.AuthViewSet, basename="auth")
router.register(r"users", views.UserViewSet)
router.register(r"courses", views.CourseViewSet)
router.register(r"lessons", views.LessonViewSet)
router.register(r"homeworks", views.HomeworkViewSet)
router.register(r"enrollments", views.EnrollmentViewSet)
router.register(r"submissions", views.HomeworkSubmissionViewSet)
router.register(r'transactions', views.TransactionViewSet, basename='transactions')

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema"),
         name="redoc"),
]
