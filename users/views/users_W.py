from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView

from users.serializers import UserSerializer, LoginSerializer
from users.models import CustomUser
from posts.models import Post



class UserViewSet(ModelViewSet):
    """_summary_

    Args:
        ModelViewSet (_type_): _modelni yaratish, o'qish, yangilash va o'chirish uchun standart CRUD operatsiyalarini ta'minlaydigan viewset.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    
class UserLoginViewSet(ModelViewSet):
    """_summary_

    Args:
        GenericViewSet (_type_): ModelViewSet kabi CRUD operatsiyalarini ta'minlamaydi, lekin custom actionlar yaratish uchun asos bo'lib xizmat qiladi.
    """
    permission_classes = [AllowAny] 
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.none()

    def get_queryset(self):
        return Post.objects.all().order_by("-created_at")


    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token), # React'da 'token' deb saqlagan joyingizga tushadi
                "refresh": str(refresh),
                "user_id": user.id,      # ID endi aniq bor
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
            }, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        


class SafeTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)

        except Exception:
            return Response(
                {"detail": "Session expired"},
                status=status.HTTP_401_UNAUTHORIZED
            )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check_password_view(request):
    user = request.user
    password = request.data.get("password")

    if not password:
        Response({"error": "parol kiritlmadi"})

    if user.check_password(password):
        return Response({"valid": True})
    
    else:
        return Response({"valid": False})


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    if not old_password:
        return Response({"error": "eski parolni kiritng"}, status=400)
    
    if not user.check_password(old_password):
        return Response({"error": "eski parol notugri"})

    user.set_password(new_password)
    user.save()

    return Response({"success": True})
    
