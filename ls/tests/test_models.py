from django.test import TestCase
from ls.models import *
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


class UserModelTest(TestCase):
    """Tests for the User model.
    Checks user creation and email uniqueness
    """

    def setUp(self) -> None:
        """Sets up a test user before each test
        """
        self.user: User = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            role="student"
        )

    def test_user_creation(self) -> None:
        """Tests that a user is created with the correct email and role
        """
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.role, "student")

    def test_email_is_unique(self) -> None:
        """Tests that creating a user with an existing email raises IntegrityError
        """
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="another",
                email="test@example.com",
                password="123"
            )

    def test_invalid_role_raises_validation_error(self) -> None:
        """Verifying that Django does not allow an invalid role through validation
        """
        user = User(
            username="hacker",
            email="hacker@test.com",
            role="super_admin_fake"
        )

        with self.assertRaises(ValidationError):
            user.full_clean()  # -> перевірить відповідність choices


class CourseModelTest(TestCase):
    """Tests for the Course model.
    Checks course creation and its relation to the instructor
    """

    def setUp(self) -> None:
        """Sets up a test instructor before each test
        """
        self.user: User = User.objects.create_user(
            username="instructor",
            email="inst@example.com",
            password="pass",
            role="instructor"
        )

    def test_create_course(self) -> None:
        """Tests the creation of a course and validates its fields
        """
        course: Course = Course.objects.create(
            instructor=self.user,
            title="Django Course",
            description="Learn Django",
            start_at="2025-01-01T00:00:00Z",
            duration=30
        )

        self.assertEqual(course.instructor, self.user)
        self.assertEqual(course.title, "Django Course")
        self.assertEqual(course.description, "Learn Django")
        self.assertEqual(course.duration, 30)


class LessonModelTest(TestCase):
    """Tests for the Lesson model
    Checks lesson creation and its relation to the instructor
    """

    def setUp(self) -> None:
        """Sets up a test lesson before each test
        """
        self.user = User.objects.create_user(
            username="inst",
            email="inst@test.com",
            password="pass",
            role="instructor"
        )

        self.course = Course.objects.create(
            instructor=self.user,
            title="Python",
            description="Course",
            start_at="2025-01-01T00:00:00Z",
            duration=10
        )

    def test_lesson_belongs_to_course(self) -> None:
        """Tests that the lesson belongs to a course
        """
        lesson = Lesson.objects.create(
            course=self.course,
            title="Intro",
            content="Basics",
            order_index=1
        )

        self.assertEqual(lesson.course, self.course)


class EnrollmentTest(TestCase):
    """Tests for the Enrollment model
    """

    def setUp(self) -> None:
        """Sets up a test enrollment before each test
        """
        self.user = User.objects.create_user(
            username="student",
            email="student@test.com",
            password="pass",
            role="student"
        )

        self.course = Course.objects.create(
            instructor=self.user,
            title="Course",
            description="Desc",
            start_at="2025-01-01T00:00:00Z",
            duration=5
        )

    def test_unique_enrollment(self) -> None:
        """Tests that the enrollment is unique
        """

        Enrollment.objects.create(
            user=self.user,
            course=self.course,
            course_status="active",
            user_progress=0,
            attendance=0
        )

        with self.assertRaises(IntegrityError):
            Enrollment.objects.create(
                user=self.user,
                course=self.course,
                course_status="active",
                user_progress=0,
                attendance=0
            )


class HomeworkSubmissionTest(TestCase):
    """Tests for the Homework submission model
    """

    def setUp(self) -> None:
        """Sets up a test homework submission before each test
        """
        self.user = User.objects.create_user(
            username="student",
            email="stud@test.com",
            password="pass",
            role="student"
        )

        self.course = Course.objects.create(
            instructor=self.user,
            title="Course",
            description="Desc",
            start_at="2025-01-01T00:00:00Z",
            duration=5
        )

        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Lesson",
            content="Content",
            order_index=1
        )

        self.homework = Homework.objects.create(
            lesson=self.lesson,
            title="HW",
            task="Do something",
            deadline="2025-01-10T00:00:00Z",
            complexity=2,
            created_by=self.user,
            deadline_date="2025-01-10"
        )

    def test_submission_creation(self) -> None:
        """Tests that the submission is created correctly
        """
        submission = HomeworkSubmission.objects.create(
            user=self.user,
            homework=self.homework
        )

        Message.objects.create(
            homework_submission=submission,
            sender=self.user,
            message_text="test"
        )

        self.assertEqual(submission.user, self.user)
        self.assertEqual(submission.homework, self.homework)


class SocialLinkModelTest(TestCase):
    """Tests for the SocialLink model
    """

    def setUp(self) -> None:
        """Sets up a test social-link before each test
        """
        self.user: User = User.objects.create_user(
            username="user1",
            email="user1@test.com",
            password="pass",
            role="student"
        )

    def test_create_social_link(self) -> None:
        """Tests creating a social link for a user
        """
        link: SocialLink = SocialLink.objects.create(
            user=self.user,
            platform_name="GitHub",
            url="https://github.com/user1"
        )

        self.assertEqual(link.user, self.user)
        self.assertEqual(link.platform_name, "GitHub")
        self.assertIn("user1@test.com", str(link))


class HomeworkModelTest(TestCase):
    """Tests for the Homework model
    """

    def setUp(self) -> None:
        """Sets up a test homework before each test
        """
        self.user: User = User.objects.create_user(
            username="inst",
            email="inst@test.com",
            password="pass",
            role="instructor"
        )

        self.course: Course = Course.objects.create(
            instructor=self.user,
            title="Course",
            description="Desc",
            start_at="2025-01-01T00:00:00Z",
            duration=10
        )

        self.lesson: Lesson = Lesson.objects.create(
            course=self.course,
            title="Lesson",
            content="Content",
            order_index=1
        )

    def test_create_homework(self) -> None:
        """Tests homework creation and relations
        """
        hw: Homework = Homework.objects.create(
            lesson=self.lesson,
            title="HW1",
            task="Solve task",
            deadline="2025-01-10T00:00:00Z",
            complexity=3,
            created_by=self.user,
            deadline_date="2025-01-10"
        )

        self.assertEqual(hw.lesson, self.lesson)
        self.assertEqual(hw.created_by, self.user)
        self.assertEqual(hw.complexity, 3)


class AIFeedbackModelTest(TestCase):
    """Tests for the AIFeedback model
    """

    def setUp(self) -> None:
        """Sets up a test ai-feedback before each test
        """
        self.user: User = User.objects.create_user(
            username="student",
            email="student@test.com",
            password="pass",
            role="student"
        )

        self.course: Course = Course.objects.create(
            instructor=self.user,
            title="Course",
            description="Desc",
            start_at="2025-01-01T00:00:00Z",
            duration=5
        )

        self.lesson: Lesson = Lesson.objects.create(
            course=self.course,
            title="Lesson",
            content="Content",
            order_index=1
        )

        self.homework: Homework = Homework.objects.create(
            lesson=self.lesson,
            title="HW",
            task="Task",
            deadline="2025-01-10T00:00:00Z",
            complexity=1,
            created_by=self.user,
            deadline_date="2025-01-10"
        )

        self.submission = HomeworkSubmission.objects.create(
            user=self.user,
            homework=self.homework
        )

        Message.objects.create(
            homework_submission=self.submission,
            sender=self.user,
            message_text="test"
        )

    def test_create_feedback(self) -> None:
        """Tests AI feedback creation
        """
        feedback: AIFeedback = AIFeedback.objects.create(
            user=self.user,
            submission=self.submission,
            feedback_text="Good job!"
        )

        self.assertEqual(feedback.user, self.user)
        self.assertEqual(feedback.submission, self.submission)
        self.assertEqual(feedback.feedback_text, "Good job!")


class TransactionModelTest(TestCase):
    """Tests for the Transaction model
    """

    def setUp(self) -> None:
        """Sets up a test transaction before each test
        """
        self.user: User = User.objects.create_user(
            username="buyer",
            email="buyer@test.com",
            password="pass",
            role="student"
        )

        self.course: Course = Course.objects.create(
            instructor=self.user,
            title="Paid Course",
            description="Desc",
            start_at="2025-01-01T00:00:00Z",
            duration=10
        )

    def test_create_transaction(self) -> None:
        """Tests transaction creation
        """
        transaction: Transaction = Transaction.objects.create(
            user=self.user,
            course=self.course,
            amount=99.99,
            status="completed",
            payment_data={"method": "card"}
        )

        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.course, self.course)
        self.assertEqual(transaction.amount, 99.99)
        self.assertEqual(transaction.status, "completed")
