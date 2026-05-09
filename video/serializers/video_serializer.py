from rest_framework import serializers
from video.models import Video
from .utils import get_video_duration_from_path   # 👈 o‘zing yozgan function

class VideoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    id       = serializers.IntegerField(read_only=True)
    likes_count = serializers.SerializerMethodField(source='get_likes_count')
    is_liked = serializers.SerializerMethodField(source='get_is_liked')
    class Meta:
        model = Video
        fields = "__all__"
        read_only_fields = ['user']

    def validate_video(self, value):
        if not value:
            raise serializers.ValidationError("Video file is required.")

        if not value.content_type.startswith("video"):
            raise serializers.ValidationError("Faqat video yuklash mumkin.")

        return value

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        user = self.context["request"].user
        return obj.likes.filter(user=user).exists()