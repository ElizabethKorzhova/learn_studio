from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import AIAdvisorSerializer
from .services import ai_advisor_response


class AIAdvisorView(APIView):
    """AI advisor view.
    API endpoint for AI-powered learning advisor.

    This view allows authenticated users to send a message
    describing their learning goals or interests and receive
    AI-generated course recommendations based on available courses
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ Handle POST request for AI advisor.

        Validates incoming data, sends user message to AI service,
        and returns generated response.

        Request body:
        { "message": "string"  # user's question or learning goal}

        Response:
        { "answer": "string"  # AI-generated recommendation}
        Raises:
            ValidationError: if request data is invalid
        """
        serializer = AIAdvisorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]

        answer = ai_advisor_response(message)

        return Response({
            "answer": answer
        })
