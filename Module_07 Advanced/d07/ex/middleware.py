from django.shortcuts import redirect
from django.urls import resolve, Resolver404
from django.contrib.auth.forms import AuthenticationForm

class LoginFormMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            request.login_form = AuthenticationForm()
        response = self.get_response(request)
        return response

class RedirectToArticlesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # No redirigir si es una petición POST
            if request.method == 'POST':
                return self.get_response(request)
            
            resolve(request.path)
            response = self.get_response(request)
            return response
        except Resolver404:
            return redirect('articles')
