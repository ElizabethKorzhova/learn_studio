from rest_framework import serializers


class AIAdvisorSerializer(serializers.Serializer):
    """Ai advisor serializer
    This serializer allows you to serialize an AI advisor
    """
    message = serializers.CharField()


class AIChatSerializer(serializers.Serializer):
    """Ai chat serializer
    This serializer allows you to serialize an AI chat"""
    message = serializers.CharField()
