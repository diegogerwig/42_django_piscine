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
