from rest_framework import serializers
from chat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)
    receiver_username = serializers.CharField(source="receiver.username", read_only=True)

    class Meta:
        model  = Message
        fields = ["id", "sender", "receiver", "content", "sender_username", "receiver_username", "created_at", "updated_at", "is_seen", "is_edited"]
