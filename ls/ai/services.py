from openai import OpenAI
import os
from dotenv import load_dotenv

from ls.models import Course

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ai_advisor_response(message):
    """Ai advisor response.
    """
    courses = Course.objects.all()

    courses_text = "\n".join([
        f"{c.id}. {c.title} - {c.description}"
        for c in courses
    ])

    prompt = f"""
    You are an AI learning advisor.

    Your job:
    - ask questions if needed
    - recommend courses ONLY from the list
    - explain why

    Courses:
    {courses_text}

    User:
    {message}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful career mentor."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
