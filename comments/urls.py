from django.urls import path, include
from rest_framework.routers import DefaultRouter

from comments.views import CommentsViewSet


router = DefaultRouter()
router.register(r"comments", CommentsViewSet, basename="comment")

urlpatterns = [
    path('', include(router.urls))
]