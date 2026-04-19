from django.test import TestCase
from unittest.mock import patch, MagicMock

from ls.ai.services import ai_advisor_response
from ls.models import Course, User
from django.utils import timezone


class AIAdvisorTest(TestCase):
    """Test suite for AI Advisor service.
    """

    def setUp(self):
        """Create initial test data:
        - instructor user
        - one default course
        """
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

    @patch("ls.ai.services.client.chat.completions.create")
    def test_ai_advisor_returns_response(self, mock_openai):
        """Test that AI advisor returns a valid response string
        and includes course recommendation.
        """
        mock = MagicMock()
        mock.choices = [
            MagicMock(message=MagicMock(content="Try Python Basics course"))
        ]
        mock_openai.return_value = mock

        result = ai_advisor_response("I want to learn programming")

        self.assertIn("Python Basics", result)

    @patch("ls.ai.services.client.chat.completions.create")
    def test_courses_in_prompt(self, mock_openai):
        """Test that available courses are correctly included
        in the prompt sent to OpenAI.
        """

        def fake_create(*args, **kwargs):
            messages = kwargs.get("messages", [])
            prompt = messages[1]["content"]

            self.assertIn("Python Basics", prompt)

            mock = MagicMock()
            mock.choices = [
                MagicMock(message=MagicMock(content="ok"))
            ]
            return mock

        mock_openai.side_effect = fake_create

        ai_advisor_response("help me choose")

    @patch("ls.ai.services.client.chat.completions.create")
    def test_no_courses(self, mock_openai):
        """Test behavior when there are no courses in database:
        - prompt still contains 'Courses' section
        - no course names appear
        - function returns AI response correctly
        """
        Course.objects.all().delete()

        def fake_create(*args, **kwargs):
            messages = kwargs.get("messages", [])
            prompt = messages[1]["content"]

            self.assertIn("Courses:", prompt)
            self.assertNotIn("Python Basics", prompt)

            mock = MagicMock()
            mock.choices = [
                MagicMock(message=MagicMock(content="No courses available"))
            ]
            return mock

        mock_openai.side_effect = fake_create

        result = ai_advisor_response("help")

        self.assertEqual(result, "No courses available")

    @patch("ls.ai.services.client.chat.completions.create")
    def test_multiple_courses_in_prompt(self, mock_openai):
        """Test that multiple courses are correctly included
        in the generated prompt.
        """
        Course.objects.create(
            instructor=self.user,
            title="Django Advanced",
            description="Deep dive",
            start_at=timezone.now(),
            duration=20
        )

        def fake_create(*args, **kwargs):
            messages = kwargs.get("messages", [])
            prompt = messages[1]["content"]

            self.assertIn("Python Basics", prompt)
            self.assertIn("Django Advanced", prompt)

            mock = MagicMock()
            mock.choices = [
                MagicMock(message=MagicMock(content="ok"))
            ]
            return mock

        mock_openai.side_effect = fake_create

        ai_advisor_response("recommend")

    @patch("ls.ai.services.client.chat.completions.create")
    def test_ai_response_not_empty(self, mock_openai):
        """Test that AI advisor always returns a non-empty response.
        """
        mock = MagicMock()
        mock.choices = [
            MagicMock(message=MagicMock(content="Try Python Basics course"))
        ]
        mock_openai.return_value = mock

        result = ai_advisor_response("I want to learn")

        self.assertTrue(len(result) > 0)
