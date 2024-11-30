from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from account.forms.auth_forms import LoginForm, RegisterForm
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from chat.models.chat_models import UserStatus


@ensure_csrf_cookie
def account_view(request):
    return render(request, 'account.html')

@csrf_protect
@require_http_methods(["POST"])
def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        try:
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            # UserStatus will be created automatically via signal
            return JsonResponse({
                'status': 'success',
                'username': user.username
            })
        except:
            return JsonResponse({
                'status': 'error',
                'errors': {'username': ['Registration failed. Please try again.']}
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'errors': form.errors
    }, status=400)

@csrf_protect
@require_http_methods(["POST"])
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        try:
            user = User.objects.get(username=username)
            status = UserStatus.get_or_create_status(user)
            
            # Check if user is already online
            if status.is_online:
                return JsonResponse({
                    'status': 'error',
                    'errors': {'__all__': ['This user is already logged in on another device or browser.']}
                }, status=400)
            
            # Attempt authentication
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'status': 'success',
                    'username': user.username
                })
        except User.DoesNotExist:
            pass
        
        return JsonResponse({
            'status': 'error',
            'errors': {'__all__': ['Invalid username or password']}
        }, status=400)
    return JsonResponse({
        'status': 'error',
        'errors': form.errors
    }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    if request.user.is_authenticated:
        status = UserStatus.get_or_create_status(request.user)
        status.is_online = False
        status.save()
    logout(request)
    return redirect('account')