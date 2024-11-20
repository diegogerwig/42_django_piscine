from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import JsonResponse
from ..models.chat_models import ChatRoom, Message

def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []
    for session in active_sessions:
        data = session.get_decoded()
        user_ids.append(data.get('_auth_user_id', None))
    return User.objects.filter(id__in=user_ids)

@login_required(login_url='account')
def room_list(request):
    """Display list of available chat rooms."""
    rooms = ChatRoom.objects.all().prefetch_related('message_set')
    for room in rooms:
        room.user_message_count = room.message_set.exclude(user__username='System').count()
    context = {
        'rooms': rooms
    }
    return render(request, 'chat/room_list.html', context)

@login_required
def chat_room(request, room_name):
    """Display chat room with message history."""
    try:
        room = ChatRoom.objects.get(name=room_name)
        rooms = ChatRoom.objects.all().prefetch_related('message_set')
        
        for r in rooms:
            r.user_message_count = r.message_set.exclude(user__username='System').count()
            
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

@login_required
def get_chat_messages(request, room_name):
    """API endpoint to get historical messages for a room."""
    try:
        room = ChatRoom.objects.get(name=room_name)
        messages = Message.objects.filter(room=room).order_by('timestamp')
        
        messages_data = [{
            'username': message.user.username,
            'message': message.content,
            'timestamp': message.timestamp.strftime('%H:%M')
        } for message in messages]
        
        return JsonResponse(messages_data, safe=False)
    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)