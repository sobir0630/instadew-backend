from rest_framework import serializers
from posts.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    # Allow clients to omit the picture field (for updates) and to clear it via `null`.
    picture  = serializers.ImageField(required=False, allow_null=True)
    username = serializers.CharField(source="user.username", read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model            = Post
        fields           = ["id", "user_id", "username", "picture", "caption", "location", "tags", "created_at", "likes_count", "is_liked", "comments_count"]
        read_only_fields = ["id", "user_id", "username", "created_at", "likes_count", "comments_count"]

    def update(self, instance, validated_data):
        # Allow clearing the picture by sending {"picture": null} or {"picture": ""}
        if "picture" in validated_data and not validated_data.get("picture"):
            if instance.picture:
                instance.picture.delete(save=False)
            instance.picture = None
            validated_data.pop("picture", None)

        return super().update(instance, validated_data)
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        user = self.context["request"].user
        return obj.likes.filter(user=user).exists()
    

class UserPostSerilizer(serializers.ModelSerializer):
    picture = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Post
        fields = "__all__"