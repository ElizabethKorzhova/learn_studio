from .ai_core import ai_chat
from ls.models import AIChatMessage


def ai_main_service(user, message: str, session_id):
    """
    Main AI service with short-term memory (ChatGPT-like behavior).
    """

    # 1. Save user message
    AIChatMessage.objects.create(user=user, session_id=session_id, role="user", content=message)
    # 2. Get last messages (memory window)
    history = AIChatMessage.objects.filter(user=user, session_id=session_id).order_by("-created_at")[:10]
    history = list(reversed(history))
    # 3. Build messages for LS
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant for an LS platform. Help users with learning, courses, payments, and support."
        }
    ]

    for msg in history:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    # 4. Call AI
    answer = ai_chat(messages)
    # 5. Save assistant response
    AIChatMessage.objects.create(user=user, session_id=session_id, role="assistant", content=answer)

    return answer
