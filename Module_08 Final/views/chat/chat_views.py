from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.sessions.models import Session
from ..models.chat_models import ChatRoom, Message, UserStatus

@login_required
def room_list(request):
    """Display list of available chat rooms."""
    rooms = ChatRoom.objects.all().prefetch_related('message_set')
    for room in rooms:
        room.user_message_count = room.message_set.exclude(user__username='System').count()
    
    # Get or create user status
    status, _ = UserStatus.objects.get_or_create(user=request.user)
    status.is_online = True
    status.session_key = request.session.session_key
    status.last_activity = timezone.now()
    status.save()
    
    context = {
        'rooms': rooms,
        'current_user': request.user
    }
    return render(request, 'chat/room_list.html', context)

@login_required
def chat_room(request, room_name):
    """Display chat room with message history."""
    try:
        room = ChatRoom.objects.get(name=room_name)
        room.users.add(request.user)
        
        rooms = ChatRoom.objects.all().prefetch_related('message_set')
        for r in rooms:
            r.user_message_count = r.message_set.exclude(user__username='System').count()
        
        # Get valid sessions
        valid_sessions = Session.objects.filter(expire_date__gt=timezone.now())
        valid_session_keys = set(s.session_key for s in valid_sessions)
        
        # Get active users
        users = []
        for user in room.users.all():
            status, _ = UserStatus.objects.get_or_create(user=user)
            if (status.is_online and status.session_key and 
                status.session_key in valid_session_keys):
                users.append({
                    'username': user.username,
                    'is_online': True
                })
            else:
                status.is_online = False
                status.session_key = None
                status.save()
        
        # Update current user's status
        status, _ = UserStatus.objects.get_or_create(user=request.user)
        status.is_online = True
        status.session_key = request.session.session_key
        status.last_activity = timezone.now()
        status.save()
        
        messages = Message.objects.filter(room=room).order_by('-timestamp')[:50]
        messages = reversed(list(messages))
        
        context = {
            'room': room,
            'rooms': rooms,
            'messages': messages,
            'users': users,
            'current_user': request.user
        }
        return render(request, 'chat/chat_room.html', context)
        
    except ChatRoom.DoesNotExist:
        return redirect('chat:room_list')

@login_required
def get_chat_messages(request, room_name):
    try:
        room = ChatRoom.objects.get(name=room_name)
        messages = Message.objects.filter(room=room).order_by('timestamp')
        
        messages_data = [{
            'username': message.user.username,
            'message': message.content,
            'timestamp': timezone.localtime(message.timestamp).strftime('%H:%M')
        } for message in messages]
        
        return JsonResponse(messages_data, safe=False)
    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)

@login_required
def get_room_users(request, room_name):
    """API endpoint to get users in a room."""
    try:
        room = ChatRoom.objects.get(name=room_name)
        
        # Get valid sessions
        valid_sessions = Session.objects.filter(expire_date__gt=timezone.now())
        valid_session_keys = set(s.session_key for s in valid_sessions)
        
        users = []
        for user in room.users.all():
            if user.is_authenticated:
                status, _ = UserStatus.objects.get_or_create(user=user)
                if (status.is_online and status.session_key and 
                    status.session_key in valid_session_keys):
                    users.append({
                        'username': user.username,
                        'is_online': True
                    })
                else:
                    status.is_online = False
                    status.session_key = None
                    status.save()
                
        return JsonResponse(users, safe=False)
    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)