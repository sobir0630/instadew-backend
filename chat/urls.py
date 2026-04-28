from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat.views import MessageViewSet, message_history, clear_history


router = DefaultRouter()
router.register(r"message", MessageViewSet, basename="message")


urlpatterns = [
    path('', include(router.urls)),
    path('history/', message_history, name="history"),
    path('history/clear/', clear_history, name="history-clear")
]