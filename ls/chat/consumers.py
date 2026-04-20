"""WebSocket consumers for chat-related functionality."""
from typing import Any

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from ls.models import Homework, Enrollment, User
from ls.chat.utils import create_chat_name


class HomeworkChatConsumer(AsyncJsonWebsocketConsumer):
    """Consumer for handling real-time chat between students and instructors"""
    chat_name: str
    homework_id: int

    async def connect(self) -> None:
        """Authenticate the user and establish a WebSocket connection"""
        user = self.scope.get("user")
        if not user or user.is_anonymous:
            await self.close(code=4401)
            return

        query_params = self.scope.get("query_params", {})

        requested_student_id = query_params.get("student_id", [None])[0]

        try:
            self.homework_id = int(self.scope["url_route"]["kwargs"]["homework_id"])
        except (ValueError, KeyError):
            await self.close(code=4400)
            return

        student_id = await self._get_student_id(
            user_id=user.id,
            user_role=user.role,
            homework_id=self.homework_id,
            requested_student_id=requested_student_id,
        )

        if student_id is None:
            await self.close(code=4403)
            return

        self.chat_name = create_chat_name(
            homework_id=self.homework_id,
            student_id=student_id,
        )

        await self.channel_layer.group_add(self.chat_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        """Close the websocket connection"""
        chat_name = getattr(self, "chat_name", None)
        if chat_name:
            await self.channel_layer.group_discard(chat_name, self.channel_name)

    async def chat_message(self, event: Any) -> None:
        """Send a chat message to the user"""
        await self.send_json({
            "type": "chat_message",
            "message": event["message"],
        })

    @database_sync_to_async
    def _get_student_id(self, *, user_id: int, user_role: str, homework_id: int,
                        requested_student_id: str | None = None) -> int | None:
        """
        Returns the student_id for the chat group

        Args:
            user_id: user id
            user_role: user role
            homework_id: homework id
            requested_student_id: requested student id
        Returns:
            student id
        """
        try:
            homework = Homework.objects.select_related(
                "lesson__course"
            ).get(id=homework_id)
        except Homework.DoesNotExist:
            return None

        course = homework.lesson.course

        if user_role == "student":
            is_enrolled = Enrollment.objects.filter(
                course=course, user_id=user_id
            ).exists()
            return user_id if is_enrolled else None

        if user_role == "instructor":
            if course.instructor_id != user_id or not requested_student_id:
                return None
            try:
                student_id = int(requested_student_id)
            except (TypeError, ValueError):
                return None

            is_enrolled = Enrollment.objects.filter(
                course=course, user_id=student_id
            ).exists()
            return student_id if is_enrolled else None
        return None
