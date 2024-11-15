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
