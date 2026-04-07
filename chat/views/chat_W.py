from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from chat.serializers import MessageSerializer
from chat.models import Message


class MessageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class   = MessageSerializer
    queryset           = Message.objects.all()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def message_history(request):
    room = request.query_params.get("room")
    if not room:
        return Response([])
    users = room.split("_")
    messages = Message.objects.filter(
        (Q(sender__username=users[0]) & Q(receiver__username=users[1])) |
        (Q(sender__username=users[1]) & Q(receiver__username=users[0]))
    ).order_by("created_at")
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def clear_history(request):
    room = request.query_params.get("room")
    if not room:
        return Response({'error': "room not entry"})
    
    try:
        users = room.split("_")
    except ValueError:
        return Response({'error': "wrong room!"})
    print("room", users)
    if request.user.username not in users:
        return Response({'error': "no permission"})

    try: 
        messages = Message.objects.filter(
            (Q(sender__username=users[0]) & Q(receiver__username=users[1])) |
            (Q(sender__username=users[1]) & Q(receiver__username=users[0]))
        )
        print("message", messages)
    except Exception as e:
        print("xatolik", e)

    print("message", messages)
    count = messages.count()
    print("COUNT:", count)
    messages.delete()

    return Response({'message': f"{count} th message deleted"})
