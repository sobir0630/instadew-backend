from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from posts.serializers import PostSerializer
from posts.models import Post, Like


class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class   = PostSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Post.objects.all().order_by("-created_at")
    
    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like = Like.objects.filter(user=user, post=post).first()

        if like:
            like.delete()
            return Response({"status": "unliked"})
        else:
            Like.objects.create(user=user, post=post)
            return Response({"status": "liked"})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserPostsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')

        # Faqat login qilgan user o'z postlarini ko'rsin
        if str(self.request.user.id) != str(user_id):
            return Post.objects.none()

        # Foydalanuvchiga tegishli postlarni olish
        return Post.objects.filter(user_id=user_id).order_by('-created_at')