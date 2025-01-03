#!/bin/sh

project_name="d06"
app_name="ex"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
app_urls_file="$app_name/urls.py"
app_forms_file="$app_name/forms.py"
project_urls_file="$project_name/urls.py"
app_models_file="$app_name/models.py"
templates_dir_app="$app_name/templates/$app_name"
templates_files="
    ../templates/$app_name/base.html
    ../templates/$app_name/nav.html
    ../templates/$app_name/index.html
    ../templates/$app_name/auth_form.html"
management_dir="$app_name/management/commands"
app_admin_file="$app_name/admin.py"
app_utils_file="$app_name/utils.py"



# Change to the project directory.
cd "$project_name"



# Create a Django app in the project.
python manage.py startapp "$app_name"
echo "✅ $app_name APP created."



# Add the app to the INSTALLED_APPS list in the settings.py file of the project.
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n    'django_bootstrap5',\n&/" "$settings_file"
echo "✅ $app_name added to INSTALLED_APPS."



# Add 'localhost' & '127.0.0.1' to the ALLOWED_HOSTS list in the settings.py file of the project.
sed -i "s/ALLOWED_HOSTS = \[.*\]/ALLOWED_HOSTS = ['localhost', '127.0.0.1']/" "$settings_file"
echo "✅ <localhost> and <127.0.0.1> added to ALLOWED_HOSTS."



# Create a URL pattern in the urls.py file of the project.
sed -i "1i\\from django.urls.conf import include" "$project_urls_file"

NEW_URL="path('', include('$app_name.urls')),"
sed -i "/urlpatterns = \[/,/]/ s|]|    $NEW_URL\n]|" "$project_urls_file"

echo "✅ URL pattern created in $project_urls_file."



# Create a new database configuration in the settings.py file of the project.
env_code=$(cat << 'EOF'
import environ
import os
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
env_file_path = os.path.join(BASE_DIR, '..', '.env')
environ.Env.read_env(env_file_path)

EOF
)

echo "$env_code" | cat - "$settings_file" | tee "$settings_file" > /dev/null

new_db_config="DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}"

temp_file=$(mktemp)

in_databases_block=false

while IFS= read -r line; do
    if [[ "$line" == "DATABASES = {" ]]; then
        in_databases_block=true
        echo "$new_db_config" >> "$temp_file"
        while IFS= read -r line && [[ "$line" != "}" ]]; do :; done
    elif [[ "$line" == "}" ]] && $in_databases_block; then
        in_databases_block=false
    else
        echo "$line" >> "$temp_file"
    fi
done < "$settings_file"

mv "$temp_file" "$settings_file"

echo "✅ Database configuration updated in $settings_file."



# Add BOOTSTRAP5 settings to the settings.py file of the project.
cat << 'EOL' >> "$settings_file"
BOOTSTRAP5 = {
    "css_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        "integrity": "sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
        "crossorigin": "anonymous",
    },
    "javascript_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",
        "crossorigin": "anonymous",
    }
}
EOL
echo "✅ BOOTSTRAP CONFIG created in $settings_file."



# Add USERS NAMES to the settings.py file of the project.
cat << 'EOL' >> "$settings_file"
SESSION_COOKIE_AGE = 42
SESSION_SAVE_EVERY_REQUEST = True 

USER_NAMES = [
    'visitor_1',
    'visitor_2',
    'visitor_3',
    'visitor_4',
    'visitor_5',
    'visitor_6',
    'visitor_7',
    'visitor_8',
    'visitor_9',
    'visitor_10',  
]

EOL
echo "✅ USER NAMES created in $settings_file."



# Create a view in the views.py file of the app.
cat << 'EOL' >> "$views_file"
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

EOL
echo "✅ VIEWS created in $views_file."



# Create a URL pattern in the urls.py file of the app.
cat << 'EOL' >> "$app_urls_file"
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
	path('signup/', views.signup, name='signup'),
	path('logout/', views.logout, name='logout'),
]

EOL
echo "✅ URL pattern created in $app_urls_file."



# Create the forms.py file to the app.
cat << 'EOL' >> "$app_forms_file"
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from .models import Tip

User = get_user_model()

class SignupForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    verif_password = forms.CharField(required=True, widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        verif_password = cleaned_data.get('verif_password')
        
        if username and User.objects.filter(username=username).exists():
            self.add_error('username', "The name entered is already taken")
        
        if password and verif_password and password != verif_password:
            self.add_error('password', "The password must be identical in the 2 password fields")
        
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password")
        
        return cleaned_data

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your tip here...'}),
        }

EOL
echo "✅ FORMS file created in $app_forms_file."



# Create models in the models.py file of the app
cat << 'EOL' > "$app_models_file"
from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class CustomGroup(Group):
    manual_can_downvote = models.BooleanField(default=False, verbose_name="Can Downvote (Group)")
    manual_can_delete = models.BooleanField(default=False, verbose_name="Can Delete (Group)")

    class Meta:
        verbose_name = 'Custom Group'
        verbose_name_plural = 'Custom Groups'

class User(AbstractUser):
    reputation = models.IntegerField(default=0)
    can_downvote_by_reputation = models.BooleanField(default=False)
    can_delete_by_reputation = models.BooleanField(default=False)
    manual_can_downvote = models.BooleanField(default=False, verbose_name="Can Downvote (Manual)")
    manual_can_delete = models.BooleanField(default=False, verbose_name="Can Delete (Manual)")

    class Meta:
        permissions = [
            ("can_downvote", "Can downvote tips from other users"),
            ("can_delete", "Can delete tips from other users"),
        ]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_group_permissions_status(self):
        """Obtiene los permisos de los grupos del usuario"""
        can_downvote = False
        can_delete = False
        for group in self.groups.all():
            try:
                custom_group = CustomGroup.objects.get(id=group.id)
                if custom_group.manual_can_downvote:
                    can_downvote = True
                if custom_group.manual_can_delete:
                    can_delete = True
            except CustomGroup.DoesNotExist:
                continue
        return can_downvote, can_delete

    def can_downvote(self):
        group_can_downvote, _ = self.get_group_permissions_status()
        return (self.has_perm('ex.can_downvote') or 
                self.can_downvote_by_reputation or 
                self.manual_can_downvote or 
                group_can_downvote)

    def can_delete(self):
        _, group_can_delete = self.get_group_permissions_status()
        return (self.has_perm('ex.can_delete') or 
                self.can_delete_by_reputation or 
                self.manual_can_delete or
                group_can_delete)

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    upvote = models.ManyToManyField(User, related_name='upvoted_tips')
    downvote = models.ManyToManyField(User, related_name='downvoted_tips')

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')} {self.content} by {self.author.username}"

EOL
echo "✅ MODELS created in $app_models_file."



# Add AUTH_USER_MODEL to the settings.py file of the project.
cat << 'EOL' >> "$settings_file"
AUTH_USER_MODEL = 'ex.User'  

EOL
echo "✅ AUTH USER MODEL created in $settings_file."



# Create the admin.py file to the app.
cat << 'EOL' >> "$app_admin_file"
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html

from .models import User, Tip, CustomGroup

class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'manual_can_downvote', 'manual_can_delete', 'get_members')
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Permissions', {
            'fields': (
                'manual_can_downvote',
                'manual_can_delete',
                'permissions',
            ),
        }),
    )

    def get_members(self, obj):
        members = User.objects.filter(groups__id=obj.id)
        return format_html(
            '<br>'.join(
                '<a href="{}">{}</a>'.format(
                    reverse('admin:ex_user_change', args=[member.id]),
                    member.username
                )
                for member in members
            )
        ) if members.exists() else 'No members'
    get_members.short_description = 'Group Members'

class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': (
            'reputation', 
            'can_downvote_by_reputation', 
            'can_delete_by_reputation',
            'manual_can_downvote',
            'manual_can_delete'
        )}),
    )
    readonly_fields = ('reputation', 'can_downvote_by_reputation', 'can_delete_by_reputation')
    list_display = ('username', 'email', 'reputation', 'can_downvote_by_reputation', 
                   'can_delete_by_reputation', 'manual_can_downvote', 'manual_can_delete')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        from .utils import update_user_reputation
        update_user_reputation(obj)

admin.site.unregister(Group)
admin.site.register(CustomGroup, CustomGroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tip)

EOL
echo "✅ ADMIN file created in $app_admin_file."



# Create the utils.py file to the app.
cat << 'EOL' >> "$app_utils_file"
from django.db.models import Count

def update_user_reputation(user):
    upvotes = user.tip_set.aggregate(total_upvotes=Count('upvote'))['total_upvotes']
    downvotes = user.tip_set.aggregate(total_downvotes=Count('downvote'))['total_downvotes']
    user.reputation = upvotes * 5 - downvotes * 2
    
    user.can_downvote_by_reputation = user.reputation >= 15
    user.can_delete_by_reputation = user.reputation >= 30
    
    user.save(update_fields=['reputation', 'can_downvote_by_reputation', 'can_delete_by_reputation'])

def toggle_vote(tip, user, vote_type):
    if vote_type not in ['upvote', 'downvote']:
        raise ValueError("vote_type must be either 'upvote' or 'downvote'")
    
    if vote_type == 'downvote' and not (user.can_downvote() or tip.author == user):
        return False
    
    opposite_type = 'downvote' if vote_type == 'upvote' else 'upvote'
    vote_manager = getattr(tip, vote_type)
    opposite_manager = getattr(tip, opposite_type)
    
    if user in vote_manager.all():
        vote_manager.remove(user)
    else:
        opposite_manager.remove(user)
        vote_manager.add(user)
    
    update_user_reputation(tip.author)
    return True

EOL
echo "✅ UTILS file created in $app_utils_file."



# Create the templates directory and files for the app.
mkdir -p "$templates_dir_app"
for template in $templates_files; do
    if [ -f "$template" ]; then
        cp "$template" "$templates_dir_app/"
        echo "✅ Copied $template to $templates_dir_app/"
    else
        echo "❗ File not found: $template"
    fi
done
echo "✅ TEMPLATES created in $templates_dir_app."



# Create a management command to populate the database
mkdir -p "$management_dir"
touch "$management_dir/__init__.py"

cat << 'EOL' > "$management_dir/populate_db.py"
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ex.models import Tip, CustomGroup
from ex.utils import toggle_vote
from django.utils import timezone
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with superuser, users, group and tips'

    def handle(self, *args, **kwargs):
        admin_username = 'admin'
        admin_password = 'pwd'
        
        User.objects.filter(username=admin_username).delete()
        
        superuser = User.objects.create_superuser(
            username=admin_username,
            password=admin_password,
            email='admin@example.com'
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser created: {admin_username}'))

        CustomGroup.objects.filter(name='Privileged Users').delete()
        
        privileged_group = CustomGroup.objects.create(
            name='Privileged Users',
            manual_can_downvote=True,
            manual_can_delete=True
        )
        self.stdout.write(self.style.SUCCESS(f'Group created: Privileged Users with special permissions'))

        usernames = ['user1', 'user2', 'user3']
        password = 'pwd'

        for username in usernames:
            User.objects.filter(username=username).delete()
            
            user = User.objects.create_user(
                username=username,
                password=password
            )
            user.groups.add(privileged_group)
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f'User created and added to group: {username}'))

        tips = [
            "Always comment your code.",
            "Use version control systems like Git.",
            "Test your code regularly.",
            "Keep your functions small and focused.",
            "Learn keyboard shortcuts for your IDE.",
            "Automate repetitive tasks.",
            "Write self-documenting code.",
            "Stay updated with the latest technologies.",
            "Collaborate and share knowledge with others.",
            "Take regular breaks to avoid burnout."
        ]

        for i in range(10):
            author = User.objects.get(username=random.choice(usernames))
            content = tips[i]
            
            tip = Tip.objects.create(
                content=content,
                author=author
            )
            
            for _ in range(random.randint(0, 5)):
                voter = random.choice(User.objects.all())
                toggle_vote(tip, voter, random.choice(['upvote', 'downvote']))

            self.stdout.write(self.style.SUCCESS(f'Successfully created tip: "{content}" by {author.username}'))

        self.stdout.write(self.style.SUCCESS('Database population completed successfully.'))
        self.stdout.write(self.style.SUCCESS(f'\nSuperuser credentials:\nUsername: {admin_username}\nPassword: {admin_password}'))
        self.stdout.write(self.style.SUCCESS(f'Regular users password: {password}'))

EOL
echo "✅ MANAGEMENT COMMAND created to populate the database."


echo -e "\n**********************\n"
