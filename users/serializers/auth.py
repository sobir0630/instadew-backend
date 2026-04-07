from rest_framework import serializers
from users.models import CustomUser, UserLogin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        ref_name = "CustomUserSerializer"

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email        = validated_data["email"],
            username     = validated_data["username"],
            full_name    = validated_data["full_name"],
            password     = validated_data["password"],
        )
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = ["id", "username", "password"]



