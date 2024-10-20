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
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from .models import CustomUser


def get_current_user(request):
    if request.user.is_authenticated:
        return request.user
    start_time = timezone.now().timestamp()
    cycle_duration = 42  # segundos
    user_names = settings.USER_NAMES
    current_cycle = int(start_time / cycle_duration) % len(user_names)
    return user_names[current_cycle]


def home(request):
    current_user = get_current_user(request)
    time_remaining = 42 - (int(timezone.now().timestamp()) % 42)
    
    tips = Tip.objects.select_related('author').prefetch_related(
        'upvote', 'downvote',
        Prefetch('author', queryset=CustomUser.objects.all())
    ).order_by('-date')
    
    form = TipForm()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if 'deletetip' in request.POST:
            tip = get_object_or_404(Tip, id=request.POST['tipid'])
            if request.user.can_delete() or tip.author == request.user:
                tip.remove_votes()
                tip.delete()
        elif 'upvote' in request.POST:
            tip = get_object_or_404(Tip, id=request.POST['tipid'])
            tip.upvoteForUser(request.user)
        elif 'downvote' in request.POST:
            tip = get_object_or_404(Tip, id=request.POST['tipid'])
            if request.user.can_downvote() or tip.author == request.user:
                tip.downvoteForUser(request.user)
        else:
            form = TipForm(request.POST)
            if form.is_valid():
                tip = form.save(commit=False)
                tip.author = request.user
                tip.save()
                request.user.update_reputation()
                return redirect('home')
    
    for tip in tips:
        tip.formatted_date = tip.date.strftime('%Y-%m-%d %H:%M:%S')
        if request.user.is_authenticated:
            tip.user_upvoted = tip.user_has_upvoted(request.user)
            tip.user_downvoted = tip.user_has_downvoted(request.user)
        tip.author.update_reputation()
        tip.author.update_user_permissions()
    
    if request.user.is_authenticated:
        request.user.update_reputation()
        request.user.update_user_permissions()
    
    context = {
        'user_name': current_user.username if request.user.is_authenticated else current_user,
        'user_reputation': current_user.reputation if request.user.is_authenticated else None,
        'tips': tips,
        'form': form,
        'session_time_remaining': time_remaining,
        'is_authenticated': request.user.is_authenticated,
        'user': request.user if request.user.is_authenticated else None,
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

