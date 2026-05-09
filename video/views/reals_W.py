from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from video.models import Video
from video.serializers import VideoSerializer


class RealsVideoViewSet(ReadOnlyModelViewSet):
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