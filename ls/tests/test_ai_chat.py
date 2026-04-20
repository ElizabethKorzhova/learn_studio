import pytest
import uuid
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.utils import timezone

from ls.ai.services.ai_main import ai_main_service
from ls.ai.services.router import detect_intent
from ls.ai.services.advisor import ai_advisor_response
from ls.models import AIChatMessage, Course

User = get_user_model()


@pytest.fixture
def user(db):
    """Creates a test user for authentication and AI interactions.
    """
    return User.objects.create_user(
        username="test",
        email="test@test.com",
        password="123456"
    )


@pytest.fixture
def course(db, user):
    """Creates a sample course for advisor-related tests.
    Ensures all required fields are populated.
    """
    return Course.objects.create(
        title="Python",
        description="Learn Python",
        instructor=user,
        price=100,
        start_at=timezone.now(),
        duration=10
    )


@pytest.mark.django_db
@patch("ls.ai.services.ai_main.ai_chat")
def test_ai_main_service_saves_messages(mock_ai_chat, user):
    """Test that ai_main_service:
    - Returns AI response
    - Saves both user and assistant messages
    - Associates messages with correct session_id
    """
    mock_ai_chat.return_value = "AI response"

    session_id = uuid.uuid4()

    response = ai_main_service(
        user=user,
        message="Hello",
        session_id=session_id
    )

    assert response == "AI response"

    messages = AIChatMessage.objects.filter(user=user, session_id=session_id)

    assert messages.count() == 2
    assert messages.first().role == "user"
    assert messages.last().role == "assistant"


@pytest.mark.django_db
@patch("ls.ai.services.ai_main.ai_chat")
def test_ai_main_service_uses_history(mock_ai_chat, user):
    """ Test that multiple calls to ai_main_service:
    - Accumulate conversation history
    - Persist messages correctly in the database
    """
    mock_ai_chat.return_value = "AI response"

    session_id = uuid.uuid4()

    ai_main_service(user=user, message="First", session_id=session_id)
    ai_main_service(user=user, message="Second", session_id=session_id)

    messages = AIChatMessage.objects.filter(user=user, session_id=session_id)

    assert messages.count() == 4


@patch("ls.ai.services.router.ai_chat")
def test_detect_intent_advisor(mock_ai_chat):
    """Test that detect_intent correctly classifies advisor-related queries.
    """
    mock_ai_chat.return_value = "advisor"

    result = detect_intent("Which course should I choose?")

    assert result == "advisor"


@patch("ls.ai.services.router.ai_chat")
def test_detect_intent_support(mock_ai_chat):
    """Test that detect_intent correctly classifies support-related queries.
    """
    mock_ai_chat.return_value = "support"

    result = detect_intent("I can't login")

    assert result == "support"


@patch("ls.ai.services.router.ai_chat")
def test_detect_intent_general(mock_ai_chat):
    """Test that detect_intent correctly classifies general queries.
    """
    mock_ai_chat.return_value = "general"

    result = detect_intent("Hello")

    assert result == "general"


@pytest.mark.django_db
@patch("ls.ai.services.advisor.ai_chat")
def test_ai_advisor_response_with_courses(mock_ai_chat, course):
    """Test that advisor returns relevant course recommendations
    when courses exist in the database.
    """
    mock_ai_chat.return_value = "Try Python course"

    response = ai_advisor_response("I want to learn programming")

    assert "Python" in response


@pytest.mark.django_db
@patch("ls.ai.services.advisor.ai_chat")
def test_ai_advisor_response_no_courses(mock_ai_chat):
    """Test that advisor handles empty course list correctly.
    """
    mock_ai_chat.return_value = "No courses found"

    response = ai_advisor_response("I want to learn")

    assert response == "No courses found"


@pytest.mark.django_db
@patch("ls.ai.services.ai_main.ai_chat")
def test_ai_history_limit_10_messages(mock_ai_chat, user):
    """Test that only the last 10 messages are sent to the AI model,
    even if more messages exist in the database.
    """
    mock_ai_chat.return_value = "AI response"

    session_id = uuid.uuid4()

    # Create more than 10 messages
    for i in range(15):
        ai_main_service(
            user=user,
            message=f"Message {i}",
            session_id=session_id
        )

    assert AIChatMessage.objects.filter(session_id=session_id).count() == 30

    # Inspect last AI call arguments
    called_args = mock_ai_chat.call_args[0][0]

    assert len(called_args) == 11

    assert called_args[-1]["content"] == "Message 14"
