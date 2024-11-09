from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from account.forms.auth_forms import LoginForm, RegisterForm
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt

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
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'username': user.username
            })
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
    logout(request)
    return redirect('account')