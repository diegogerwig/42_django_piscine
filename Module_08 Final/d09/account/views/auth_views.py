from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.db import transaction, IntegrityError
from chat.models.chat_models import UserStatus
from account.forms.auth_forms import LoginForm, RegisterForm
from django.utils import timezone
from ..forms.auth_forms import RegisterForm

@ensure_csrf_cookie
def account_view(request):
    return render(request, 'account.html')


@csrf_protect
@require_http_methods(["POST"])
def login_view(request):
    form = LoginForm(request=request, data=request.POST)
    if form.is_valid():
        login(request, form.get_user())
        return JsonResponse({
            'status': 'success',
            'username': form.get_user().username,
            'redirect': '/chat/'
        })
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@csrf_protect
@require_http_methods(["POST"])
def register_view(request):
    if User.objects.filter(username=request.POST.get('username')).exists():
        return JsonResponse({
            'status': 'error',
            'errors': {'username': ['Username already taken']}
        }, status=400)

    form = RegisterForm(request.POST)
    if form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(request, user)
        return JsonResponse({
            'status': 'success',
            'username': user.username,
            'redirect': '/chat/'
        })

    return JsonResponse({
        'status': 'error',
        'errors': form.errors
    }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    if request.user.is_authenticated:
        try:
            status = UserStatus.objects.get_or_create(user=request.user)[0]
            status.is_online = False
            status.session_key = None
            status.save()
        except Exception as e:
            print(f"Logout error: {str(e)}")
    logout(request)
    return redirect('account')