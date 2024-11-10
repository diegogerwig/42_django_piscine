from django.shortcuts import render
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
    room = ChatRoom.objects.get(name=room_name)
    messages = Message.objects.filter(room=room)
    return render(request, 'chat_room.html', {
        'room': room,
        'messages': messages
    })