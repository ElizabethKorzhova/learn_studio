from django.test import TestCase
from unittest.mock import patch

from ls.ai.services import ai_advisor_response
from ls.models import Course, User
from django.utils import timezone


class AIAdvisorTest(TestCase):
    """Test suite for AI Advisor service.
    """

    def setUp(self):
        """Create initial test data."""
        self.user = User.objects.create(
            email="test@test.com",
            username="test",
            role="instructor"
        )

        self.course = Course.objects.create(
            instructor=self.user,
            title="Python Basics",
            description="Learn Python from scratch",
            start_at=timezone.now(),
            duration=10
        )

    @patch("ls.ai.services.ai_chat")
    def test_ai_advisor_returns_response(self, mock_ai_chat):
        """AI returns response with course name."""
        mock_ai_chat.return_value = "Try Python Basics course"

        result = ai_advisor_response("I want to learn programming")

        self.assertIn("Python Basics", result)

    @patch("ls.ai.services.ai_chat")
    def test_courses_in_prompt(self, mock_ai_chat):
        """Courses должны передаваться в prompt."""

        def fake_ai_chat(messages):
            prompt = messages[1]["content"]

            self.assertIn("Python Basics", prompt)
            return "ok"

        mock_ai_chat.side_effect = fake_ai_chat

        ai_advisor_response("help me choose")

    @patch("ls.ai.services.ai_chat")
    def test_no_courses(self, mock_ai_chat):
        """Behavior when no courses exist."""
        Course.objects.all().delete()

        def fake_ai_chat(messages):
            prompt = messages[1]["content"]

            self.assertIn("Courses:", prompt)
            self.assertNotIn("Python Basics", prompt)

            return "No courses available"

        mock_ai_chat.side_effect = fake_ai_chat

        result = ai_advisor_response("help")

        self.assertEqual(result, "No courses available")

    @patch("ls.ai.services.ai_chat")
    def test_multiple_courses_in_prompt(self, mock_ai_chat):
        """Multiple courses appear in prompt."""
        Course.objects.create(
            instructor=self.user,
            title="Django Advanced",
            description="Deep dive",
            start_at=timezone.now(),
            duration=20
        )

        def fake_ai_chat(messages):
            prompt = messages[1]["content"]

            self.assertIn("Python Basics", prompt)
            self.assertIn("Django Advanced", prompt)

            return "ok"

        mock_ai_chat.side_effect = fake_ai_chat

        ai_advisor_response("recommend")

    @patch("ls.ai.services.ai_chat")
    def test_ai_response_not_empty(self, mock_ai_chat):
        """AI response should not be empty."""
        mock_ai_chat.return_value = "Some response"

        result = ai_advisor_response("I want to learn")

        self.assertTrue(len(result) > 0)
