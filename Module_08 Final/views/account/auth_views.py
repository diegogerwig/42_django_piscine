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
def register_view(request):
    print("==================== New Registration Attempt ====================")
    print("Received registration data:", request.POST)
    
    # Validate form before any database operations
    form = RegisterForm(request.POST)
    if not form.is_valid():
        print("Form validation errors:", form.errors)
        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        }, status=400)

    username = form.cleaned_data['username']
    try:
        with transaction.atomic():
            # Delete any existing user and status with this username
            User.objects.filter(username=username).delete()
            
            # Create new user
            user = User.objects.create_user(
                username=username,
                password=form.cleaned_data['password']
            )
            print(f"Successfully created user: {username}")

            # Delete any existing status for this user and create a new one
            UserStatus.objects.filter(user=user).delete()
            user_status = UserStatus.objects.create(
                user=user,
                is_online=True,
                session_key=request.session.session_key,
                last_activity=timezone.now()
            )
            print(f"Successfully created UserStatus for: {username}")

            # Login the user
            login(request, user)
            print(f"Successfully logged in user: {username}")

            return JsonResponse({
                'status': 'success',
                'username': username,
                'redirect': '/chat/'
            })

    except IntegrityError as e:
        print(f"IntegrityError during registration: {str(e)}")
        # Clean up any partially created data
        User.objects.filter(username=username).delete()
        return JsonResponse({
            'status': 'error',
            'errors': {'username': ['Registration failed. Please try again.']}
        }, status=400)
        
    except Exception as e:
        print(f"Unexpected error during registration: {str(e)}")
        # Clean up any partially created data
        User.objects.filter(username=username).delete()
        return JsonResponse({
            'status': 'error',
            'errors': {'__all__': ['An unexpected error occurred. Please try again.']}
        }, status=500)
    
    finally:
        print("==================== End Registration Attempt ====================")


@csrf_protect
@require_http_methods(["POST"])
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                status = UserStatus.objects.get_or_create(user=user)[0]
                status.is_online = True
                status.session_key = request.session.session_key
                status.save()
                return JsonResponse({
                    'status': 'success',
                    'username': user.username
                })
        except Exception as e:
            print(f"Login error: {str(e)}")
            
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
        try:
            status = UserStatus.objects.get_or_create(user=request.user)[0]
            status.is_online = False
            status.session_key = None
            status.save()
        except Exception as e:
            print(f"Logout error: {str(e)}")
    logout(request)
    return redirect('account')