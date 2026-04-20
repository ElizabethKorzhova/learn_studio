from django.urls import path
from .views import AIAdvisorView, AIChatView

urlpatterns = [
    path("advisor/", AIAdvisorView.as_view(), name="ai-advisor"),
    path("chat/", AIChatView.as_view(), name="ai-chat"),
]
