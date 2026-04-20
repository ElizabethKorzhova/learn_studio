from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import AIAdvisorSerializer
from .services.ai_main import ai_main_service


class AIAdvisorView(APIView):
    """Legacy advisor endpoint (can be kept or removed later).
    Now powered by AI engine.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AIAdvisorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]

        session_id = request.headers.get("X-Session-ID") or str(request.user.id)

        answer = ai_main_service(
            user=request.user,
            message=message,
            session_id=session_id
        )

        return Response({
            "answer": answer
        })


class AIChatView(APIView):
    """Main AI chat endpoint
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AIAdvisorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]

        session_id = request.headers.get("X-Session-ID") or str(request.user.id)

        answer = ai_main_service(
            user=request.user,
            message=message,
            session_id=session_id
        )

        return Response({
            "answer": answer
        })
