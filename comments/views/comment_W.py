from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from comments.serializers import IsOwner
from comments.models import Comments
from comments.serializers import CommentSerialzers


class CommentsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class   = CommentSerialzers
    queryset = Comments.objects.all()

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        if post_id:
            return self.queryset.filter(post_id=post_id).order_by('-created_at')
        return self.queryset.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]