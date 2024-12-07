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

# import logging

# logger = logging.getLogger(__name__)

# @csrf_protect
# @require_http_methods(["POST"])
# def register_view(request):
#     logger.debug(f"Received data: {request.POST}")

#     if request.user.is_authenticated:
#         # Redirect logged-in users to another page
#         logger.info(f"User {request.user.username} is already logged in. Redirecting to /chat/")
#         return redirect('/chat/') 

#     form = RegisterForm(request.POST)

#     # Validate the form first
#     if form.is_valid():
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
        
#         # Now check if username is already taken (form should already have validated the data)
#         if User.objects.filter(username=username).exists():
#             logger.warning(f"Username {username} already taken.")
#             return JsonResponse({
#                 'status': 'error',
#                 'errors': {'username': ['Username already taken']}
#             }, status=400)

#         try:
#             with transaction.atomic():
#                 # Create user if no error
#                 user = User.objects.create_user(username=username, password=password)
#                 login(request, user)  # Log in the user after registration
#                 logger.info(f"User {user.username} created and logged in successfully.")
#                 return redirect('/chat/')
#         except IntegrityError as e:
#             logger.error(f"Database error: {e}")
#             return JsonResponse({
#                 'status': 'error',
#                 'errors': {'username': ['Database error, please try again.']}
#             }, status=400)
    
#     # If the form is not valid, log the errors and return them
#     logger.error(f"Form errors: {form.errors}")
#     return JsonResponse({
#         'status': 'error',
#         'errors': form.errors
#     }, status=400)


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            return JsonResponse({'message': 'Username and password are required'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already taken'}, status=400)

        try:
            user = User.objects.create_user(username=username, password=password)

            login(request, user)
            return JsonResponse({'redirect': '/chat/'}, status=200)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid method'}, status=405)


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