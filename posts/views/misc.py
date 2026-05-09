from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from posts.serializers import UserPostSerilizer
from posts.models import Post
from users.models import CustomUser


User = CustomUser

class UserProfileView(ReadOnlyModelViewSet):
    serializer_class = UserPostSerilizer

    def get_queryset(self):
        username = self.request.query_params.get("username")

        if not username:
            return Post.objects.none()
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Post.objects.none()
        
        return Post.objects.filter(user=user).order_by("-created_at")
