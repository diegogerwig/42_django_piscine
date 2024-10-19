from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Tip, Upvote, Downvote
from .forms import SignupForm, LoginForm, TipForm
from django.forms.models import model_to_dict
import random

def get_current_user(request):
    if request.user.is_authenticated:
        return request.user.username
    start_time = timezone.now().timestamp()
    cycle_duration = 42  # segundos
    user_names = settings.USER_NAMES
    current_cycle = int(start_time / cycle_duration) % len(user_names)
    return user_names[current_cycle]

def home(request):
    current_user = get_current_user(request)
    time_remaining = 42 - (int(timezone.now().timestamp()) % 42)
    
    if request.method == 'POST':
        if 'deletetip' in request.POST:
            if (request.user.has_perm('ex.deletetip') or
                    model_to_dict(Tip.objects.get(
                        id=request.POST['tipid'])).get('author') ==
                    request.user.username):
                Tip.objects.filter(id=request.POST['tipid']).delete()
        elif 'upvote' in request.POST:
            ts = Tip.objects.filter(id=request.POST['tipid'])
            if ts.exists():
                ts.first().upvoteForUser(request.user.username)
        elif 'downvote' in request.POST:
            ts = Tip.objects.filter(id=request.POST['tipid'])
            if ts.exists():
                ts.first().downvoteForUser(request.user.username)
        else:
            form = TipForm(request.POST)
            if form.is_valid():
                tip = form.save(commit=False)
                tip.author = request.user.username if request.user.is_authenticated else current_user
                tip.save()
                return redirect('home')
    else:
        form = TipForm()
    
    tips = Tip.objects.all().order_by('-date')
    for tip in tips:
        tip.formatted_date = tip.date.strftime('%Y-%m-%d %H:%M:%S')
    
    context = {
        'user_name': current_user,
        'tips': tips,
        'form': form,
        'session_time_remaining': time_remaining,
        'is_authenticated': request.user.is_authenticated
    }
    
    return render(request, 'ex/index.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = auth.authenticate(username=data['username'], password=data['password'])
            if user and user.is_active:
                auth.login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'ex/auth_form.html', {
        'user_name': get_current_user(request),
        'form': form,
        'is_authenticated': request.user.is_authenticated,
        'session_time_remaining': 42 - (int(timezone.now().timestamp()) % 42)
    })

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user.save()
            auth.login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'ex/auth_form.html', {
        'user_name': get_current_user(request),
        'form': form,
        'is_authenticated': request.user.is_authenticated,
        'session_time_remaining': 42 - (int(timezone.now().timestamp()) % 42)
    })



def logout(request):
    auth.logout(request)
    return redirect('home')

