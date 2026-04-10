"""LMS Administration Module.
This module defines the configuration of the admin panel and the registration of models."""
from typing import List, Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ModelChoiceField
from django.http import HttpRequest
from django.db.models import ForeignKey

from .models import (User, Course, Lesson, Homework, HomeworkSubmission,
                     Enrollment, SocialLink, AIFeedback, Transaction, Message)


class SocialLinkInline(admin.TabularInline):
    """Inline representation of SocialLink model for UserAdmin."""
    model = SocialLink
    extra = 1


class CourseInline(admin.StackedInline):
    """Inline representation of Course model for UserAdmin."""
    model = Course
    extra = 1


class HomeworkInline(admin.StackedInline):
    """Inline representation of Homework model for LessonAdmin."""
    model = Homework
    extra = 1


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for the User model."""
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {"fields": ("role", "phone", "avatar")}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "role", "first_name", "last_name"),
        }),
    )

    list_display = ("username", "email", "role")
    readonly_fields = ["id", "created_at"]

    inlines = [SocialLinkInline]
    instructor_inlines = [SocialLinkInline, CourseInline]

    list_filter = ("role",)
    search_help_text = "Search by the username or the email"
    search_fields = ("username", "email")

    def get_inline_instances(self, request: HttpRequest, obj: User | None = None) \
            -> List[admin.options.InlineModelAdmin]:
        """Returns inline instances based on the role of the user.
        Instructors can see their courses; others can see only their social links."""
        inline_classes = self.instructor_inlines if obj and obj.role == "instructor" \
            else self.inlines
        return [inline(self.model, self.admin_site) for inline in inline_classes]


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """Admin configuration for the SocialLink model."""
    list_display = ("user__username", "user__email", "platform_name")
    readonly_fields = ["id"]

    list_filter = ("platform_name",)
    search_help_text = "Search by the username or the email"
    search_fields = ("user__username", "user__email")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for the CourseAdmin model."""
    list_display = ("title", "instructor", "price", "duration", "start_at")
    readonly_fields = ["id", "created_at"]

    search_help_text = "Search by the title of the the course"
    search_fields = ("title",)

    def formfield_for_foreignkey(self, db_field: ForeignKey, request: HttpRequest,
                                 **kwargs: Any) -> ModelChoiceField | None:
        """Filters the users dropdown in course to display only users with the instructor role."""
        if db_field.name == "instructor":
            kwargs["queryset"] = User.objects.filter(role="instructor")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for the Lesson model."""
    list_display = ("order_index", "title", "course__title", "course__instructor__email")
    readonly_fields = ["id"]

    inlines = [HomeworkInline]

    search_help_text = "Search by the title of the lesson or the course"
    search_fields = ("title", "course__title")


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    """Admin configuration for the Homework model."""
    list_display = ("title", "complexity", "deadline_date", "lesson__order_index",
                    "lesson__course__title", "created_by__email")
    readonly_fields = ["id"]

    search_help_text = "Search by the title of the homework"
    search_fields = ("title",)


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    """Admin configuration for the HomeworkSubmission model."""
    list_display = ("user__username", "user__email", "homework__title", "score",
                    "homework__created_by__email")
    readonly_fields = ("id", "submitted_at")

    search_help_text = "Search by the title of the homework or the username or the email"
    search_fields = ("homework__title", "user__username", "user__email",
                     "homework__created_by__email")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin configuration for the Message model."""
    list_display = ("homework_submission__homework__title", "sender__username", "sender__email", "created_at")
    readonly_fields = ("id", "created_at")

    search_help_text = "Search by the username or the email of the sender"
    search_fields = ("sender__username", "sender__email")


@admin.register(AIFeedback)
class AIFeedbackAdmin(admin.ModelAdmin):
    """Admin configuration for the AIFeedback model."""
    list_display = ("user__username", "user__email", "submission__homework__title", "created_at")
    readonly_fields = ("id", "created_at")

    search_help_text = "Search by the username or the email of the student"
    search_fields = ("user__username", "user__email")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin configuration for the EnrollmentAdmin model."""
    list_display = ("user__username", "user__email", "course__title",
                    "course_status", "user_progress", "course__instructor__email")
    readonly_fields = ("id", "enrolled_at", "updated_at")

    list_filter = ("course_status", "enrolled_at")
    search_help_text = ("Search by the title of the course or the username "
                        "or the email of the student")
    search_fields = ("course__title", "user__username", "user__email")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin configuration for the Transaction model."""
    list_display = ("user__email", "course__title", "amount", "status")
    readonly_fields = ("id", "created_at")

    list_filter = ("status",)
    search_help_text = "Search by the title of the course or the email of the student"
    search_fields = ("course__title", "user__email")
