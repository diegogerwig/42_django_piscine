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
views_source_dir="views/chat"
models_source_dir="models/chat"
templates_source_dir="templates/chat"
scripts_source_dir="scripts/chat"
consumers_source_dir="consumers/chat"

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

# Update ALLOWED_HOSTS to allow all IPs
sed -i "s/ALLOWED_HOSTS = .*/ALLOWED_HOSTS = ['*']/" "$settings_file"
echo "✅ Allowed hosts updated to accept all IPs."

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

# Add Static Files configuration
if ! grep -q "STATIC_URL" "$settings_file"; then
    cat << 'EOL' >> "$settings_file"

# Static files configuration
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "chat/scripts"),
]
EOL
    echo "✅ Static files configuration added."
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
copy_directory_contents "$views_source_dir"         "$views_dir_app"        "VIEWS"
copy_directory_contents "$models_source_dir"        "$models_dir_app"       "MODELS"
copy_directory_contents "$templates_source_dir"     "$templates_dir_app"    "TEMPLATES"
copy_directory_contents "$scripts_source_dir"       "$scripts_dir"          "SCRIPTS"
copy_directory_contents "$consumers_source_dir"     "$consumers_dir_app"    "CONSUMERS"

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
    path('chat/scripts/<path:path>', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'chat', 'scripts')
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
from .views.chat_views import room_list, chat_room, get_chat_messages, get_room_users
from django.http import HttpResponse
import os

app_name = 'chat'

def serve_js(request, filename):
    js_files = {
        'chat-core.js': 'chat/scripts/chat-core.js',
        'chat-websocket.js': 'chat/scripts/chat-websocket.js',
        'chat-init.js': 'chat/scripts/chat-init.js'
    }
    
    if filename in js_files:
        file_path = js_files[filename]
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return HttpResponse(file.read(), content_type='application/javascript')
    return HttpResponse(status=404)

urlpatterns = [
    path('', room_list, name='room_list'),
    path('chat/', room_list, name='room_list'),
    path('room/<str:room_name>/', chat_room, name='chat_room'),
    path('api/<str:room_name>/messages/', get_chat_messages, name='chat_messages'),
    path('api/<str:room_name>/users/', get_room_users, name='room_users'),
    path('scripts/<str:filename>', serve_js, name='serve_js'),
]
EOL
echo "✅ Chat URLs created."

# Create middleware directory and file
mkdir -p "$app_name/middleware"
touch "$app_name/middleware/__init__.py"

# Create middleware.py with updated code
cat << 'EOL' > "$app_name/middleware/middleware.py"
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

class SessionUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Initialize the required middleware
        self.session_middleware = SessionMiddleware(self.get_response)
        self.auth_middleware = AuthenticationMiddleware(self.get_response)

    def __call__(self, request):
        # Ensure session is available
        if not hasattr(request, 'session'):
            self.session_middleware(request)
        
        # Ensure user is available
        if not hasattr(request, 'user'):
            self.auth_middleware(request)

        # Now we can safely check authentication
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                session = Session.objects.get(
                    session_key=request.session.session_key
                )
                request.user.session = session
            except Session.DoesNotExist:
                pass
        
        response = self.get_response(request)
        return response
EOL

# Update middleware in settings.py
if ! grep -q "SessionUpdateMiddleware" "$settings_file"; then
    sed -i "/MIDDLEWARE = \[/a\    'chat.middleware.middleware.SessionUpdateMiddleware'," "$settings_file"
    echo "✅ Session middleware created and added to settings."
fi

# Create asgi.py
cat << 'EOL' > "$project_name/asgi.py"
import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'd09.settings')
django.setup()

from chat.routing import websocket_urlpatterns

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
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

echo -e "\n🏠 Created rooms:"
echo "- room1"
echo "- room2"
echo "- room3"

echo -e "\n👤 Created users (password for all: urduliz):"
echo "- user1"
echo "- user2"
echo "- user3"
echo "- user4"
echo "- user5"

echo -e "\n✨ CHAT application setup complete!\n"

echo -e "\n**********************\n"