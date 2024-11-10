#!/bin/sh

# Directory names
project_name="d09"
app_name="chat"

# Project files paths
settings_file="$project_name/settings.py"
project_urls_file="$project_name/urls.py"

# App directory structure
views_dir_app="$app_name/views"
models_dir_app="$app_name/models"
templates_dir_app="$app_name/templates"
consumers_dir_app="$app_name/consumers"

# Source directories (current directory)
views_source_dir="views/chat"
models_source_dir="models/chat"
templates_source_dir="templates/chat"
consumers_source_dir="consumers/chat"

# Create Django app
cd "$project_name"
python manage.py startapp "$app_name"
echo "✅ <$app_name> APP created."

# Create directory structure
mkdir -p "$views_dir_app"
mkdir -p "$models_dir_app"
mkdir -p "$templates_dir_app"
mkdir -p "$consumers_dir_app"

# Create __init__.py files
touch "$views_dir_app/__init__.py"
touch "$models_dir_app/__init__.py"
touch "$consumers_dir_app/__init__.py"

# Add Channels and App to INSTALLED_APPS
if ! grep -q "'channels'," "$settings_file"; then
    sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n    'channels',\n&/" "$settings_file"
    echo "✅ Apps added to INSTALLED_APPS."
fi

# Add Channels configuration
if ! grep -q "ASGI_APPLICATION" "$settings_file"; then
    cat << 'EOL' >> "$settings_file"

# Channels configuration
ASGI_APPLICATION = 'd09.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
EOL
    echo "✅ Channels configuration added."
fi

# Update project URLs to add chat while keeping account paths
cat << 'EOL' > "$project_urls_file"
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
import os
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),  # Account debe ir primero para manejar login/registro
    path('scripts/<path:path>', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'account', 'scripts')
    }),
    path('chat/', include('chat.urls')),  # Chat en /chat/
]
EOL
echo "✅ Project URLs created."

# Create routing.py in chat app
cat << 'EOL' > "$app_name/routing.py"
from django.urls import re_path
from .consumers.chat_consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_accept),
]
EOL
echo "✅ Chat routing created."

# Create urls.py in chat app
cat << 'EOL' > "$app_name/urls.py"
from django.urls import path
from .views.chat_views import room_list, chat_room

urlpatterns = [
    path('', room_list, name='room_list'),  # /chat/
    path('<str:room_name>/', chat_room, name='chat_room'),  # /chat/room-name/
]
EOL
echo "✅ Chat URLs created."

# Update views to use account login
cat << 'EOL' > "$app_name/views/chat_views.py"
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models.chat_models import ChatRoom, Message

@login_required(login_url='login')
def room_list(request):
    """Display list of available chat rooms."""
    rooms = ChatRoom.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

@login_required(login_url='login')
def chat_room(request, room_name):
    """Display chat room with message history."""
    try:
        room = ChatRoom.objects.get(name=room_name)
        messages = Message.objects.filter(room=room)
        return render(request, 'chat_room.html', {
            'room': room,
            'messages': messages
        })
    except ChatRoom.DoesNotExist:
        return redirect('room_list')
EOL
echo "✅ Views updated."

# Create models
cat << 'EOL' > "$app_name/models/chat_models.py"
from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
EOL
echo "✅ Models created."

# Create consumer
cat << 'EOL' > "$app_name/consumers/chat_consumer.py"
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from ..models.chat_models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f'{self.scope["user"].username} has joined the chat',
                    'username': 'System'
                }
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.scope["user"].username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    @database_sync_to_async
    def save_message(self, message):
        room = ChatRoom.objects.get(name=self.room_name)
        Message.objects.create(
            room=room,
            user=self.scope["user"],
            content=message
        )
EOL
echo "✅ Consumer created."

# Create templates
cat << 'EOL' > "$app_name/templates/room_list.html"
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block content %}
<div class="container mt-4">
    <h2>Chat Rooms</h2>
    <div class="list-group">
        {% for room in rooms %}
            <a href="{% url 'chat_room' room.name %}" class="list-group-item list-group-item-action">
                {{ room.name }}
            </a>
        {% endfor %}
    </div>
</div>
{% endblock %}
EOL
echo "✅ Room list template created."

# Create chat room template
cat << 'EOL' > "$app_name/templates/chat_room.html"
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block extra_head %}
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<style>
    #chat-log {
        height: 400px;
        overflow-y: auto;
        margin-bottom: 20px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    .message {
        margin-bottom: 10px;
    }
    .username {
        font-weight: bold;
        color: #007bff;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>Chat Room: {{ room.name }}</h2>
    <div id="chat-log">
        {% for message in messages %}
            <div class="message">
                <span class="username">{{ message.user.username }}:</span>
                <span class="content">{{ message.content }}</span>
            </div>
        {% endfor %}
    </div>
    <div class="input-group">
        <input type="text" id="chat-message-input" class="form-control" placeholder="Type your message...">
        <button id="chat-message-submit" class="btn btn-primary">Send</button>
    </div>
</div>

<script>
    const roomName = "{{ room.name }}";
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const message = `
            <div class="message">
                <span class="username">${data.username}:</span>
                <span class="content">${data.message}</span>
            </div>
        `;
        $('#chat-log').append(message);
        $('#chat-log').scrollTop($('#chat-log')[0].scrollHeight);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    $('#chat-message-input').focus();
    $('#chat-message-input').on('keyup', function(e) {
        if (e.keyCode === 13) {  // enter key
            $('#chat-message-submit').click();
        }
    });

    $('#chat-message-submit').on('click', function(e) {
        const messageInputDom = $('#chat-message-input');
        const message = messageInputDom.val();
        if (message) {
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.val('');
        }
    });
</script>
{% endblock %}
EOL
echo "✅ Chat room template created."

# Create asgi.py
cat << 'EOL' > "$project_name/asgi.py"
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'd09.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
EOL
echo "✅ ASGI configuration created."

# Create migrations and apply them
python manage.py makemigrations
python manage.py migrate

# Create initial chat rooms
python manage.py shell << 'EOL'
from chat.models.chat_models import ChatRoom
if not ChatRoom.objects.filter(name='General').exists():
    ChatRoom.objects.create(name='General')
if not ChatRoom.objects.filter(name='Random').exists():
    ChatRoom.objects.create(name='Random')
if not ChatRoom.objects.filter(name='Support').exists():
    ChatRoom.objects.create(name='Support')
EOL
echo "✅ Initial chat rooms created."

echo -e "\n✨ Chat application setup complete!"
echo -e "\n📝 Don't forget to:"
echo "1. Install channels: pip install channels"
echo "2. Verify all files were created correctly"
echo "3. Run the server: python manage.py runserver"