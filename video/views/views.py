from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models.post_model import Post
from video.models import Video, Like
from video.serializers import VideoSerializer
from video.serializers.utils import get_video_duration_from_path


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user

        if not user or not user.is_authenticated:
            return Video.objects.none() 

        if user.is_superuser:
            return Video.objects.all()

        return Video.objects.all()
    
    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        video = self.get_object()
        user = request.user

        like = Like.objects.filter(user=user, video=video).first()

        if like:
            like.delete()
            return Response({"status": "unliked"})
        else:
            Like.objects.create(user=user, video=video)
            return Response({"status": "liked"})

    def perform_create(self, serializer):
        file = self.request.FILES.get("video")

        if not file:
            raise ValidationError("Video file required")

        if not file.content_type.startswith("video"):
            raise ValidationError("Faqat video yuklash mumkin")

        # 1. SAVE QILISH (AVVAL)
        video_obj = serializer.save(user=self.request.user)

        path = video_obj.video.path

        print("VIDEO OBJECT:", video_obj)
        print("VIDEO PATH:", path)

        # 3. DURATION HISOBLASH
        duration = get_video_duration_from_path(path)

        if not duration:
            video_obj.delete()
            raise ValidationError("Video duration aniqlanmadi")

        if duration > 120:
            video_obj.delete()
            raise ValidationError("Video 2 minutdan uzun bo‘lmasligi kerak")

        # 4. UPDATE QILISH
        video_obj.duration = duration
        video_obj.save()

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        video = self.get_object()
        user = request.user

        like = Like.objects.filter(user=user, video=video).first()

        if like:
            like.delete()
            return Response({"status": "unliked"})
        else:
            Like.objects.create(user=user, video=video)
            return Response({"status": "liked"})