"""Utility functions for chat"""
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser

from ls.models import User


def create_chat_name(*, homework_id: int, student_id: int) -> str:
    """Generates a chat name for a given homework

    Args:
        homework_id (int): homework id
        student_id (int): student id
    Returns:
        str: chat name
    """
    return f"homework_chat_{homework_id}_{student_id}"


@database_sync_to_async
def get_user_from_token(token: str) -> User | AnonymousUser:
    """
    Returns the authenticated User or AnonymousUser

    Args:
        token (str): JWT token
    Returns:
        User or AnonymousUser
    """
    authenticator = JWTAuthentication()

    try:
        token_bytes = token.encode("utf-8")
        validated_token = authenticator.get_validated_token(token_bytes)
        return authenticator.get_user(validated_token)
    except (InvalidToken, TokenError):
        return AnonymousUser()
