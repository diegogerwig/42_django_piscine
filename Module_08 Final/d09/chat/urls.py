# from django.urls import path
# from .views.chat_views import room_list, chat_room, get_chat_messages, get_room_users

# app_name = 'chat'

# urlpatterns = [
#     path('', room_list, name='room_list'),
#     path('room/<str:room_name>/', chat_room, name='chat_room'),
#     path('api/<str:room_name>/messages/', get_chat_messages, name='chat_messages'),
#     path('api/<str:room_name>/users/', get_room_users, name='room_users'),
# ]

from django.urls import path
from .views.chat_views import room_list, chat_room, get_chat_messages, get_room_users

app_name = 'chat'

urlpatterns = [
    path('', room_list, name='room_list'),
    path('room/<str:room_name>/', chat_room, name='chat_room'),
    path('api/<str:room_name>/messages/', get_chat_messages, name='chat_messages'),
    path('api/<str:room_name>/users/', get_room_users, name='room_users'),
]
