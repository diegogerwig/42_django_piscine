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

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        # Enviar mensaje de conexión
        if self.user.is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f'{self.user.username} has joined the chat',
                    'username': 'System',
                    'timestamp': timezone.now().strftime('%H:%M')
                }
            )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        if self.user.is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f'{self.user.username} has left the chat',
                    'username': 'System',
                    'timestamp': timezone.now().strftime('%H:%M')
                }
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Save message to database
        await self.save_message(message)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
                'timestamp': timezone.now().strftime('%H:%M')
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
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

