from rest_framework import serializers
from comments.models import Comments


class CommentSerialzers(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source="user.username")
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comments
        fields = "__all__"
