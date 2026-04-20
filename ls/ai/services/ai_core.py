from ..providers import groq_provider, openai_provider
import os


def ai_chat(messages: list) -> str:
    """
    Universal AI chat engine with provider fallback.
    """

    provider = os.getenv("AI_PROVIDER", "groq")

    try:
        if provider == "groq":
            return groq_provider.chat_completion(messages)

        return openai_provider.chat_completion(messages)

    except Exception:
        return openai_provider.chat_completion(messages)
