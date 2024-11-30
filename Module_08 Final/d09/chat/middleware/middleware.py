from django.contrib.sessions.models import Session
from django.utils import timezone

class SessionUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Update user's session reference
            try:
                session = Session.objects.get(session_key=request.session.session_key)
                request.user.session = session
            except Session.DoesNotExist:
                pass
        
        response = self.get_response(request)
        return response
