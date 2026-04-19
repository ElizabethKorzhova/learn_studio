from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def chat_completion(messages) -> str:
    """Send chat messages to Groq API and return the generated response
    """
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
    )
    return response.choices[0].message.content
