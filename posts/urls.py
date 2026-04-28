from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet, UserPostsView, UserProfileView



router = DefaultRouter()
router.register(r"post", PostViewSet, basename="posts"),
router.register(r"my-posts/(?P<user_id>\d+)", UserPostsView, basename="my-posts"),
router.register(r"profile", UserProfileView, basename="profile-data")

urlpatterns = [
    path('', include(router.urls)),
]