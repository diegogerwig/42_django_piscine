from django.urls import path
from .views.chat_views import room_list, chat_room

urlpatterns = [
    path('', room_list, name='room_list'),
    path('room/<str:room_name>/', chat_room, name='chat_room'),
]