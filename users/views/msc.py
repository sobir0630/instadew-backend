from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from users.serializers import RegisterUserViewSerializers


class RegisterUserViews(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class   = RegisterUserViewSerializers
    queryset           = CustomUser

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'username',
                openapi.IN_QUERY,
                description="User username",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )

    @action(detail=False, methods=["get"])
    def by_username(self, request):
        username = request.GET.get("username")

        if not username:
            return Response({"error": "username required"}, status=400)
        try:
            user = CustomUser.objects.get(username=username)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({'error': "user not found"})


