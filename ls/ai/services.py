import os
from ls.models import Course
from .providers import groq_provider, openai_provider


def ai_chat(messages):
    """
    Send messages to selected AI provider.
    Supports fallback to OpenAI if primary provider fails.
    """
    provider = os.getenv("AI_PROVIDER", "groq")

    try:
        if provider == "groq":
            return groq_provider.chat_completion(messages)

        return openai_provider.chat_completion(messages)

    except Exception:
        return openai_provider.chat_completion(messages)


def ai_advisor_response(message):
    """
    Generate AI-based course recommendations.

    - Uses only courses from DB
    - Prevents hallucinations
    - Sends structured prompt to AI
    """
    courses = Course.objects.all()

    courses_text = "\n".join([
        f"{c.id}. {c.title} - {c.description}"
        for c in courses
    ]) or "No courses available"

    prompt = f"""
    You are an AI learning advisor.

    STRICT RULES:
    - Recommend ONLY courses from the provided list
    - Do NOT invent new courses
    - If no suitable course, say so

    Your job:
    - ask questions if needed
    - recommend courses
    - explain why

    Courses:
    {courses_text}

    User:
    {message}
    """

    return ai_chat([
        {"role": "system", "content": "You are a helpful career mentor."},
        {"role": "user", "content": prompt},
    ])
