from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType

from comments.models import Comments
from comments.serializers import CommentSerialzers
from comments.serializers import IsOwner

from posts.models import Post
from video.models import Video


class CommentsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class   = CommentSerialzers
    queryset           = Comments.objects.all()

    def get_queryset(self):
        post_id  = self.request.query_params.get("post")
        video_id = self.request.query_params.get("video")

        if post_id:
            content_type = ContentType.objects.get_for_model(Post)
            return Comments.objects.filter(
                content_type=content_type,
                object_id=post_id
            ).order_by("-created_at")

        if video_id:
            content_type = ContentType.objects.get_for_model(Video)
            return Comments.objects.filter(
                content_type=content_type,
                object_id=video_id
            ).order_by("-created_at")

        return Comments.objects.all()

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]