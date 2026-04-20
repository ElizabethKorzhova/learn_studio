"""Channels middleware for authenticating WebSocket users via JWT."""
from typing import Any

from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

from .utils import get_user_from_token


class QueryStringJWTAuthMiddleware(BaseMiddleware):
    """Middleware to authenticate WebSocket connections using a JWT token."""

    async def __call__(self, scope: Any, receive: Any, send: Any) -> Any:
        """Handle the incoming connection and authenticate the user via JWT."""
        query_string = scope.get("query_string", b"").decode("utf-8", errors="ignore")

        query_params = parse_qs(query_string)
        scope["query_params"] = query_params

        token = query_params.get("token", [None])[0]
        scope["user"] = await get_user_from_token(token) if token else AnonymousUser()

        return await super().__call__(scope, receive, send)
