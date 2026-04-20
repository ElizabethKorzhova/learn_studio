from .ai_core import ai_chat


def detect_intent(message: str) -> str:
    """
    Classifies user intent.
    Returns: 'advisor' | 'general' | 'support'
    """

    system_prompt = """
    You are an intent classifier for an LS system.

    Return ONLY one word:
    - advisor (if user asks about courses, learning, career)
    - support (if user asks about payments, login, technical issues, manager contact)
    - general (everything else)

    Do not explain.
    """

    result = ai_chat([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ])

    return result.strip().lower()
