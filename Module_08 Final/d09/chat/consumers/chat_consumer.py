import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from ..models.chat_models import ChatRoom, Message
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope["user"]

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        if self.user.is_authenticated:
            system_message = f'{self.user.username} has joined the chat'
            await self.save_system_message(system_message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'system_message',
                    'message': system_message,
                    'timestamp': timezone.now().strftime('%H:%M')
                }
            )

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            system_message = f'{self.user.username} has left the chat'
            await self.save_system_message(system_message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'system_message',
                    'message': system_message,
                    'timestamp': timezone.now().strftime('%H:%M')
                }
            )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            
            if await self.save_message(message):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.user.username,
                        'timestamp': timezone.now().strftime('%H:%M')
                    }
                )
        except Exception as e:
            print(f"Error in receive: {e}")

    async def system_message(self, event):
        await self.send(text_data=json.dumps({
            'username': 'System',
            'message': event['message'],
            'timestamp': event['timestamp']
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def save_message(self, message):
        try:
            room = ChatRoom.objects.get(name=self.room_name)
            Message.objects.create(
                room=room,
                user=self.user,
                content=message
            )
            return True
        except Exception as e:
            print(f"Error saving message: {e}")
            return False

    @database_sync_to_async
    def save_system_message(self, message):
        try:
            room = ChatRoom.objects.get(name=self.room_name)
            system_user, _ = User.objects.get_or_create(
                username='System',
                defaults={'is_active': False}
            )
            Message.objects.create(
                room=room,
                user=system_user,
                content=message
            )
            return True
        except Exception as e:
            print(f"Error saving system message: {e}")
            return False