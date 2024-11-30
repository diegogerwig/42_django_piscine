import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.sessions.models import Session
from ..models.chat_models import ChatRoom, Message, UserStatus

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        # Clean up inactive users and check current user
        await self.cleanup_inactive_users()
        if await self.is_user_online():
            await self.close(code=4000)
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Set user as online and add to room
        await self.set_user_online(True)
        await self.add_user_to_room()
        
        # Send initial system message and update user list
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
        await self.broadcast_user_list()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Set user as offline
            await self.set_user_online(False)
            
            # Send system message
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
            await self.broadcast_user_list()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            
            if text_data_json.get('type') == 'user_offline':
                await self.set_user_online(False)
                await self.broadcast_user_list()
                return

            message = text_data_json.get('message')
            if message and await self.save_message(message):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.user.username,
                        'timestamp': timezone.now().strftime('%H:%M')
                    }
                )
                await self.broadcast_user_list()
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

    async def user_list_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_list_update',
            'users': event['users']
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

    @database_sync_to_async
    def is_user_online(self):
        status = UserStatus.get_or_create_status(self.user)
        return status.is_online and self.user.is_authenticated

    @database_sync_to_async
    def set_user_online(self, status):
        user_status = UserStatus.get_or_create_status(self.user)
        user_status.is_online = status
        user_status.last_activity = timezone.now()
        if hasattr(self.scope, "session") and self.scope.session:
            user_status.session_key = self.scope.session.session_key
        user_status.save()
        return True

    @database_sync_to_async
    def add_user_to_room(self):
        room = ChatRoom.objects.get(name=self.room_name)
        room.users.add(self.user)
        return True

    @database_sync_to_async
    def get_active_users(self):
        """Get only currently logged-in users in the room"""
        room = ChatRoom.objects.get(name=self.room_name)
        active_users = []
        
        # Get valid sessions
        valid_sessions = Session.objects.filter(expire_date__gt=timezone.now())
        valid_session_keys = [s.session_key for s in valid_sessions]
        
        for user in room.users.all():
            if user.is_authenticated:
                status = UserStatus.objects.get_or_create(user=user)[0]
                if (status.is_online and status.session_key and 
                    status.session_key in valid_session_keys):
                    active_users.append({
                        'username': user.username,
                        'is_online': True
                    })
        
        return active_users

    @database_sync_to_async
    def cleanup_inactive_users(self):
        """Clean up all users that are not currently logged in"""
        valid_sessions = Session.objects.filter(expire_date__gt=timezone.now())
        valid_session_keys = set(s.session_key for s in valid_sessions)
        
        # Update status for users with invalid sessions
        UserStatus.objects.exclude(session_key__in=valid_session_keys).update(
            is_online=False,
            session_key=None
        )

    async def broadcast_user_list(self):
        """Send updated active user list to all clients"""
        active_users = await self.get_active_users()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list_update',
                'users': active_users
            }
        )