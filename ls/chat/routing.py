"""WebSocket routes for chat-related consumers."""
from django.urls import re_path

from ls.chat.consumers import HomeworkChatConsumer

websocket_urlpatterns = [
    re_path(
        r"^ws/chat/homework/(?P<homework_id>\d+)/$",
        HomeworkChatConsumer.as_asgi(),
    ),
]
