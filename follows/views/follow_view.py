from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from follows.models import Follow
from follows.serializers.follow_serializer import FollowSerializer


User = get_user_model()

class FolowViews(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class   = FollowSerializer
    queryset           = Follow.objects.all()


    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Follow.objects.none()
        
        return Follow.objects.filter(follower=self.request.user)
    

    @action(detail=False, methods=["post"])
    def toggle(self, request):
        username = request.data.get("username")
        print("username:", request.data)
        try:
            target = User.objects.get(username=username)
            
        except User.DoesNotExist:
            return Response({'error': "User not found"}, status=404)
        
        if request.user == target:
            return Response({'error': "can't follow yourself"}, status=400)
        
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target
        )

        if not created:
            follow.delete()
            is_following = False
            
        else:
            is_following = True

        followers_count = Follow.objects.filter(following=target).count()

        return Response({
            "is_following": is_following,
            "followers_count": followers_count,
            "following": target.username
        })
        