from django.urls import path
from .views import AIAdvisorView

urlpatterns = [
    path("advisor/", AIAdvisorView.as_view(), name="ai-advisor"),
]
