import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """ این متد هنگام اتصال WebSocket اجرا می‌شود """
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

        # عضویت در گروه چت
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()  # اتصال را قبول می‌کنیم

    async def disconnect(self, close_code):
        """ این متد هنگام قطع اتصال WebSocket اجرا می‌شود """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """ این متد پیام دریافتی از کلاینت را پردازش می‌کند """
        data = json.loads(text_data)
        message = data["message"]
        sender_id = data["sender"]

        # گرفتن چت و کاربر از دیتابیس به‌صورت آسنکرون
        chat = await sync_to_async(Chat.objects.get)(id=self.chat_id)
        sender = await sync_to_async(User.objects.get)(id=sender_id)

        # ذخیره پیام در دیتابیس
        new_message = await sync_to_async(Message.objects.create)(
            chat=chat, sender=sender, text=message
        )

        # ارسال پیام به گروه WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender.username,
                "timestamp": str(new_message.timestamp)
            },
        )

    async def chat_message(self, event):
        """ این متد پیام را برای کلاینت‌ها ارسال می‌کند """
        await self.send(text_data=json.dumps(event))
