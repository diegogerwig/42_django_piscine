from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

import random

from .forms import SignupForm, LoginForm, TipForm
from .models import Tip
from .utils import update_user_reputation, toggle_vote

User = get_user_model()

def get_current_user(request):
    if request.user.is_authenticated:
        return request.user
    
    start_time = timezone.now().timestamp()
    cycle_duration = 42  # segundos
    user_names = settings.USER_NAMES
    current_cycle = int(start_time / cycle_duration) % len(user_names)
    return user_names[current_cycle]

def get_session_time_remaining(request):
    if request.user.is_authenticated:
        return None
    return 42 - (int(timezone.now().timestamp()) % 42)

def home(request):
    current_user = get_current_user(request)
    time_remaining = get_session_time_remaining(request)
    
    tips = Tip.objects.select_related('author').prefetch_related(
        'upvote', 'downvote',
        Prefetch('author', queryset=User.objects.all())
    ).order_by('-date')
    
    form = TipForm()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if 'deletetip' in request.POST:
            tip = get_object_or_404(Tip, id=request.POST['tipid'])
            if request.user.can_delete() or tip.author == request.user:
                tip.upvote.clear()
                tip.downvote.clear()
                tip.delete()
                update_user_reputation(tip.author)
        elif 'vote' in request.POST:
            tip = get_object_or_404(Tip, id=request.POST['tipid'])
            vote_type = request.POST['vote']
            if vote_type in ['upvote', 'downvote']:
                if vote_type == 'downvote' and not (request.user.can_downvote() or tip.author == request.user):
                    pass
                else:
                    toggle_vote(tip, request.user, vote_type)
            return redirect('home')
        else:
            form = TipForm(request.POST)
            if form.is_valid():
                tip = form.save(commit=False)
                tip.author = request.user
                tip.save()
                update_user_reputation(request.user)
                return redirect('home')
    
    for tip in tips:
        tip.formatted_date = tip.date.strftime('%Y-%m-%d %H:%M:%S')
        if request.user.is_authenticated:
            tip.user_upvoted = tip.upvote.filter(id=request.user.id).exists()
            tip.user_downvoted = tip.downvote.filter(id=request.user.id).exists()
        update_user_reputation(tip.author)
    
    if request.user.is_authenticated:
        update_user_reputation(request.user)
    
    context = {
        'user_name': current_user.username if request.user.is_authenticated else current_user,
        'user_reputation': current_user.reputation if request.user.is_authenticated else None,
        'tips': tips,
        'form': form,
        'is_authenticated': request.user.is_authenticated,
        'user': request.user if request.user.is_authenticated else None,
    }
    
    if not request.user.is_authenticated:
        context['session_time_remaining'] = time_remaining
    
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
    
    context = {
        'user_name': get_current_user(request),
        'form': form,
        'is_authenticated': request.user.is_authenticated,
    }
    
    time_remaining = get_session_time_remaining(request)
    if time_remaining is not None:
        context['session_time_remaining'] = time_remaining
        
    return render(request, 'ex/auth_form.html', context)

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
    
    context = {
        'user_name': get_current_user(request),
        'form': form,
        'is_authenticated': request.user.is_authenticated,
    }
    
    time_remaining = get_session_time_remaining(request)
    if time_remaining is not None:
        context['session_time_remaining'] = time_remaining
        
    return render(request, 'ex/auth_form.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')

