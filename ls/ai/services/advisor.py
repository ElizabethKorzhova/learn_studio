from ls.models import Course
from .ai_core import ai_chat


def ai_advisor_response(message: str) -> str:
    """
    Course recommendation engine.
    """

    courses = Course.objects.all()

    courses_text = "\n".join([
        f"{c.id}. {c.title} - {c.description}"
        for c in courses
    ]) or "No courses available"

    prompt = f"""
    You are an AI learning advisor.

    RULES:
    - ONLY use provided courses
    - Never invent courses
    - If nothing fits → say it

    COURSES:
    {courses_text}

    USER QUESTION:
    {message}
    """

    return ai_chat([
        {"role": "system", "content": "You are a helpful mentor."},
        {"role": "user", "content": prompt}
    ])
