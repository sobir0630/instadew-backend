from rest_framework import serializers
from users.models import CustomUser


class RegisterUserViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"