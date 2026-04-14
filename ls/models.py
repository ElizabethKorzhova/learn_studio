from django.db import models
from django.contrib.auth.models import AbstractUser


# -----USERS
class User(AbstractUser):
    """Represents a system user. A user can be a student, instructor, or admin
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


# ------SOCIAL LINKS
class SocialLink(models.Model):
    """Stores social media links associated with a user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_links")
    platform_name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self) -> str:
        return f"{self.user.email} - {self.platform_name}"


# ------COURSES
class Course(models.Model):
    """Represents an educational course created by an instructor
    """
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_at = models.DateTimeField()
    duration = models.IntegerField()  # course_long
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


# ----- LESSONS
class Lesson(models.Model):
    """Represents a single lesson within a course
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    content = models.TextField()
    order_index = models.IntegerField()
    images = models.ImageField(upload_to='lessons/', null=True, blank=True)

    def __str__(self) -> str:
        return self.title


# ------HOMEWORKS
class Homework(models.Model):
    """Represents an assignment associated with a lesson
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="homeworks")
    title = models.CharField(max_length=255)
    task = models.TextField()
    deadline = models.DateTimeField()
    complexity = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    deadline_date = models.DateField()

    def __str__(self) -> str:
        return self.title


# -----HOMEWORK SUBMISSIONS
class HomeworkSubmission(models.Model):
    """Represents a user's submission for a homework task
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name="submissions")
    # messages = models.JSONField() прибрала тому що створили окремо таблицю Messages
    files = models.FileField(upload_to='submissions/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.homework.title}"


# ------AI FEEDBACKS
class AIFeedback(models.Model):
    """Stores AI-generated feedback for a homework submission
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(HomeworkSubmission, on_delete=models.CASCADE, related_name="feedbacks")
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# ------ENROLLMENTS
class Enrollment(models.Model):
    """Tracks user participation in courses
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    course_status = models.CharField(max_length=50)
    user_progress = models.IntegerField(default=0)
    attendance = models.FloatField(default=0.0)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "course")


# -----TRANSACTIONS
class Transaction(models.Model):
    """Represents a payment made by a user for a course
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    payment_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


# -------Messages
class Message(models.Model):
    """Represents a message made by a user for homework submission
    """
    homework_submission = models.ForeignKey(
        HomeworkSubmission,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.email} -> submission {self.homework_submission.id}"

#------Progress
class LessonProgress(models.Model):
    """Tracks user progress per lesson"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="lesson_progress"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="progress"
    )

    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "lesson")

    def __str__(self):
        return f"{self.user.email} - {self.lesson.title}"