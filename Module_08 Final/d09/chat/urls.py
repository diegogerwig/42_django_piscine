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
