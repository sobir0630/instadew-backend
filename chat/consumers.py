import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from chat.models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        WebSocket ulanishi paytida chaqiriladi.
        URL dan room_name olinadi va kanal guruhiga qo'shiladi.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Kanal guruhiga qo‘shilish
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        WebSocket uzilishida chaqiriladi.
        Kanal guruhidan chiqaradi.
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        WebSocket orqali xabar qabul qilganda chaqiriladi.
        """
        data = json.loads(text_data)
        msg_type = data.get("type")

        # ---------------- Typing indikator ----------------
        if msg_type == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.typing",
                    "sender": data.get("sender")
                }
            )

        # ---------------- Oddiy xabar ----------------
        elif msg_type == "chat_message":
            msg_obj = await self.save_message(data)
            if msg_obj:
                receiver_username = msg_obj.receiver.username

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat.message",
                        "id": msg_obj.id,
                        "message": msg_obj.content,
                        "sender": msg_obj.sender.username,   # 🔥 mana bu muhim
                        "receiver": msg_obj.receiver.username,
                        "created_at": str(msg_obj.created_at),
                        # "is_online": receiver_username in online_users,
                    }
                )

        # ---------------- Xabarni o'chirish ----------------
        elif msg_type == "delete":
            await self.delete_message(data.get("id"))
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.delete",
                    "id": data.get("id")
                }
            )

        # ---------------- Xabarni tahrirlash ----------------
        elif msg_type == "edit":
            msg_obj = await self.edit_message(data.get("id"), data.get("message"))
            if msg_obj:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat.edit",
                        "id": msg_obj.id,
                        "message": msg_obj.content
                    }
                )

    # ---------------- Event handlerlar ----------------
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": event["message"],
            "sender": event["sender"],
            "created_at": event["created_at"]
        }))

    async def chat_typing(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "sender": event["sender"]
        }))

    async def chat_delete(self, event):
        await self.send(text_data=json.dumps({
            "type": "delete",
            "id": event["id"]
        }))

    async def chat_edit(self, event):
        await self.send(text_data=json.dumps({
            "type": "edit",
            "id": event["id"],
            "message": event["message"]
        }))

    # ---------------- Bazaga yozish amallari ----------------
    @sync_to_async
    def save_message(self, data):
        """
        Xabarni saqlaydi. Agar sender yoki receiver topilmasa, None qaytaradi.
        """
        try:
            sender = User.objects.get(username=data.get("sender"))
        except User.DoesNotExist:
            return None

        # Receiverni room_name orqali aniqlash (room_name "user1_user2" formatida bo‘lishi kerak)
        try:
            users = self.room_name.split("_")
            receiver_username = users[1] if users[0] == data.get("sender") else users[0]
            receiver = User.objects.get(username=receiver_username)
        except (IndexError, User.DoesNotExist):
            return None

        return Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=data.get("message", "")
        )

    @sync_to_async
    def delete_message(self, msg_id):
        Message.objects.filter(id=msg_id).delete()

    @sync_to_async
    def edit_message(self, msg_id, text):
        try:
            msg = Message.objects.get(id=msg_id)
            msg.content = text
            msg.is_edited = True
            msg.save()
            return msg
        except Message.DoesNotExist:
            return None


# Global online userlar (simple variant)
online_users = set()

class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("PRESENCE CONNECT BO‘LDI")
        user = self.scope["user"]

        if user.is_authenticated:
            self.username = user.username
            online_users.add(self.username)
            print("qushildi", online_users)

        else:
            self.username = None

        await self.accept()

        # clientga yuboramiz
        await self.send(text_data=json.dumps({
            "type": "presence",
            "online_users": list(online_users)
        }))

    async def disconnect(self, close_code):
        print("PRESENCE UZULDI")
        if self.username:
            await online_users.discard(self.username)

