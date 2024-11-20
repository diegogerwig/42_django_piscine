from django.urls import path
from .views.chat_views import room_list, chat_room, get_chat_messages

app_name = 'chat'

urlpatterns = [
    path('', room_list, name='room_list'),  # /chat/
    path('api/<str:room_name>/messages/', get_chat_messages, name='chat_messages'),  # /chat/api/<room_name>/messages/
    path('room/<str:room_name>/', chat_room, name='chat_room'),  # /chat/room/<room_name>/
]
