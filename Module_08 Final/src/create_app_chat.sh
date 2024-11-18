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
templates_dir_app="$app_name/templates/chat"  
scripts_dir="$app_name/scripts"
consumers_dir_app="$app_name/consumers"


# Source directories
templates_source_dir="templates/chat"
scripts_source_dir="scripts/chat"


# Create Django app
cd "$project_name"
python manage.py startapp "$app_name"
echo "✅ <$app_name> APP created."


# Create directory structure
mkdir -p "$views_dir_app"
mkdir -p "$models_dir_app"
mkdir -p "$templates_dir_app"
mkdir -p "$scripts_dir"
mkdir -p "$consumers_dir_app"


# Create __init__.py files
touch "$views_dir_app/__init__.py"
touch "$models_dir_app/__init__.py"
touch "$consumers_dir_app/__init__.py"


# Add Channels and App to INSTALLED_APPS
if ! grep -q "'channels'," "$settings_file" && ! grep -q "'$app_name'," "$settings_file"; then
    # Primero verificamos si django_bootstrap5 ya está en INSTALLED_APPS
    if ! grep -q "'django_bootstrap5'," "$settings_file"; then
        sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n    'channels',\n    'django_bootstrap5',\n&/" "$settings_file"
    else
        sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n    'channels',\n&/" "$settings_file"
    fi
    echo "✅ Apps added to INSTALLED_APPS."
fi


# Add Channels configuration and auth settings
if ! grep -q "ASGI_APPLICATION" "$settings_file"; then
    cat << 'EOL' >> "$settings_file"

# Channels configuration
ASGI_APPLICATION = 'd09.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Authentication settings
LOGIN_URL = '/account/'
EOL
    echo "✅ Channels and authentication configuration added."
fi


# Add Templates configuration
if ! grep -q "TEMPLATES = \[" "$settings_file"; then
    cat << 'EOL' >> "$settings_file"

# Templates configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "chat/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
EOL
    echo "✅ Templates configuration added."
else
    sed -i '/TEMPLATES.*=.*\[/,/\]/ {
        /DIRS.*:.*\[/ {
            n
            s|]|    os.path.join(BASE_DIR, "chat/templates"),\n&|
        }
    }' "$settings_file"
    echo "✅ Templates DIRS updated."
fi


# Copy files from source to destination directory function
copy_directory_contents() {
    local source_dir=$1
    local dest_dir=$2
    local dir_type=$3
    local had_errors=false

    if [ -d "../$source_dir" ]; then
        echo -e "\n📁 Copying $dir_type files from ../$source_dir:"
        
        for file in "../$source_dir"/*; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                if cp "$file" "$dest_dir/"; then
                    echo "   ✅ Copied: $filename"
                else
                    echo "   ❌ Failed to copy: $filename"
                    had_errors=true
                fi
            fi
        done
        
        if [ "$had_errors" = true ]; then
            echo "❌ Some $dir_type files failed to copy"
            return 1
        else
            echo "⭐ $dir_type copied successfully to $dest_dir/"
            return 0
        fi
    else
        echo "❗ $dir_type source directory not found: ../$source_dir"
        return 1
    fi
}


# Copy template files
copy_directory_contents "$templates_source_dir" "$templates_dir_app" "TEMPLATES"
copy_directory_contents "$scripts_source_dir" "$scripts_dir" "SCRIPTS"


# Update project URLs
cat << 'EOL' > "$project_urls_file"
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
import os
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scripts/<path:path>', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'account', 'scripts')
    }),
    path('', include('account.urls')),  # Account maintains root
    path('chat/', include('chat.urls')),  # Chat under /chat/
]
EOL
echo "✅ Project URLs created."


# Create routing.py in chat app
cat << 'EOL' > "$app_name/routing.py"
from django.urls import re_path
from .consumers.chat_consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]

EOL
echo "✅ Chat routing created."


# Create urls.py in chat app
cat << 'EOL' > "$app_name/urls.py"
from django.urls import path
from .views.chat_views import room_list, chat_room

app_name = 'chat'

urlpatterns = [
    path('', room_list, name='room_list'),  # /chat/
    path('<str:room_name>/', chat_room, name='chat_room'),  # /chat/<room_name>/
]
EOL
echo "✅ Chat URLs created."


# Create views
cat << 'EOL' > "$app_name/views/chat_views.py"
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models.chat_models import ChatRoom, Message
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []
    for session in active_sessions:
        data = session.get_decoded()
        user_ids.append(data.get('_auth_user_id', None))
    return User.objects.filter(id__in=user_ids)

@login_required
def room_list(request):
    """Display list of available chat rooms."""
    rooms = ChatRoom.objects.all()
    # Obtener solo usuarios con sesión activa
    active_users = get_current_users().exclude(is_superuser=True)
    return render(request, 'chat/room_list.html', {
        'rooms': rooms,
        'users': active_users
    })

@login_required
def chat_room(request, room_name):
    """Display chat room with message history."""
    try:
        room = ChatRoom.objects.get(name=room_name)
        rooms = ChatRoom.objects.all()
        # Obtener solo usuarios con sesión activa
        active_users = get_current_users().exclude(is_superuser=True)
        messages = Message.objects.filter(room=room).order_by('-timestamp')[:50]
        messages = reversed(list(messages))

        return render(request, 'chat/chat_room.html', {
            'room': room,
            'rooms': rooms,
            'messages': messages,
            'users': active_users,
            'current_user': request.user
        })
    except ChatRoom.DoesNotExist:
        return redirect('chat:room_list')
EOL
echo "✅ Views created."


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

EOL
echo "✅ Consumer created."


# Create asgi.py
cat << 'EOL' > "$project_name/asgi.py"
import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'd09.settings')
django.setup()  # Añade esta línea

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
EOL
echo "✅ ASGI configuration created."


# Create migrations and apply them
python manage.py makemigrations
python manage.py migrate


# Create initial chat rooms and users
python manage.py shell << 'EOL'
from chat.models.chat_models import ChatRoom
from django.contrib.auth.models import User

# Create rooms
rooms = ['room1', 'room2', 'room3']
for room_name in rooms:
    if not ChatRoom.objects.filter(name=room_name).exists():
        ChatRoom.objects.create(name=room_name)

# Create users
for i in range(1, 6):  # Creating users 1 through 5
    username = f'user{i}'
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password='urduliz')

EOL
echo "✅ Initial chat rooms and users created."

echo -e "\n👤 Created users (password for all: urduliz):"
echo "- user1"
echo "- user2"
echo "- user3"
echo "- user4"
echo "- user5"

echo -e "\n🏠 Created rooms:"
echo "- room1"
echo "- room2"
echo "- room3"

echo -e "\n✨ CHAT application setup complete!\n"

echo -e "\n**********************\n"