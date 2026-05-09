from rest_framework import serializers
from comments.models import Comments
from django.contrib.contenttypes.models import ContentType
from posts.models import Post
from video.models import Video


class CommentSerialzers(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    post_id  = serializers.IntegerField(write_only=True, required=False)
    video_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Comments
        fields = [
            "id",
            "username",
            "text",
            "post_id",
            "video_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "username", "created_at", "updated_at"]

    def validate(self, attrs):
        post_id  = attrs.get("post_id")
        video_id = attrs.get("video_id")

        if post_id and video_id:
            raise serializers.ValidationError("Faqat bitta: post_id yoki video_id yuboring")

        if not post_id and not video_id:
            raise serializers.ValidationError("post_id yoki video_id majburiy")

        return attrs

    def create(self, validated_data):
        request = self.context["request"]

        post_id = validated_data.pop("post_id", None)
        video_id = validated_data.pop("video_id", None)

        if post_id:
            obj = Post.objects.filter(id=post_id).first()
        else:
            obj = Video.objects.filter(id=video_id).first()

        if not obj:
            raise serializers.ValidationError("Post yoki Video topilmadi")

        content_type = ContentType.objects.get_for_model(obj)

        return Comments.objects.create(
            user=request.user,
            content_type=content_type,
            object_id=obj.id,
            text=validated_data["text"]
        )