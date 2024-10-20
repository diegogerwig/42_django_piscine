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


# Change to the project directory.
cd "$project_name"


# Create a Django app in the project.
python manage.py startapp "$app_name"
echo "✅ $app_name APP created."


# Add the app to the INSTALLED_APPS list in the settings.py file of the project.
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n    'django_bootstrap5',\n&/" "$settings_file"
echo "✅ $app_name added to INSTALLED_APPS."


# Add 'localhost' to the ALLOWED_HOSTS list in the settings.py file of the project.
sed -i "s/ALLOWED_HOSTS = \[.*\]/ALLOWED_HOSTS = ['localhost']/" "$settings_file"
echo "✅ localhost added to ALLOWED_HOSTS."


# Create a URL pattern in the urls.py file of the project.
sed -i "1i\\from django.urls.conf import include" "$project_urls_file"

NEW_URL="path('/', include('$app_name.urls')),"
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
    # The complete URL to the Bootstrap CSS file
    "css_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        "integrity": "sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
        "crossorigin": "anonymous",
    },

    # The complete URL to the Bootstrap JavaScript file
    "javascript_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",
        "crossorigin": "anonymous",
    },

    # The URL to the Popper JavaScript file (Bootstrap 5 uses Popper for dropdowns, tooltips, and popovers)
    # Note: Bootstrap 5 bundles Popper with its JavaScript, so this might not be necessary
    "popper_url": None,

    # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap5.html)
    "javascript_in_head": False,

    # Label class to use in horizontal forms
    "horizontal_label_class": "col-sm-3",

    # Field class to use in horizontal forms
    "horizontal_field_class": "col-sm-9",

    # Set placeholder attributes to label if no placeholder is provided
    "set_placeholder": True,

    # Class to indicate required (better to set this in your Django form)
    "required_css_class": "",

    # Class to indicate error (better to set this in your Django form)
    "error_css_class": "is-invalid",

    # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
    "success_css_class": "is-valid",

    # Renderers (only set these if you have studied the source and understand the inner workings)
    "formset_renderers":{
        "default": "django_bootstrap5.renderers.FormsetRenderer",
    },
    "form_renderers": {
        "default": "django_bootstrap5.renderers.FormRenderer",
    },
    "field_renderers": {
        "default": "django_bootstrap5.renderers.FieldRenderer",
        "inline": "django_bootstrap5.renderers.InlineFieldRenderer",
    },
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
from django.contrib.auth.models import User
from .models import Tip
from django.contrib.auth import authenticate


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
            self.add_error('verif_password', "The password must be identical in the 2 password fields")
        
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
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType


class CustomUser(AbstractUser):
    reputation = models.IntegerField(default=0)

    def update_reputation(self):
        upvotes = sum(tip.upvote.count() for tip in self.tip_set.all())
        downvotes = sum(tip.downvote.count() for tip in self.tip_set.all())
        self.reputation = upvotes * 5 - downvotes * 2
        self.save()

    def can_downvote(self):
        return self.reputation >= 15 or self.has_perm('ex.can_downvote')

    def can_delete(self):
        return self.reputation >= 30 or self.has_perm('ex.can_delete')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_user_permissions()

    def update_user_permissions(self):
        content_type = ContentType.objects.get_for_model(Tip)
        can_downvote = Permission.objects.get(
            codename='can_downvote',
            content_type=content_type,
        )
        can_delete = Permission.objects.get(
            codename='can_delete',
            content_type=content_type,
        )
        
        if self.reputation >= 15:
            self.user_permissions.add(can_downvote)
        else:
            self.user_permissions.remove(can_downvote)
        
        if self.reputation >= 30:
            self.user_permissions.add(can_delete)
        else:
            self.user_permissions.remove(can_delete)

class Upvote(models.Model):
    voted_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Downvote(models.Model):
    voted_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    upvote = models.ManyToManyField(Upvote)
    downvote = models.ManyToManyField(Downvote)

    class Meta:
        permissions = [
            ("can_delete", "Can delete tips from other users"),
            ("can_downvote", "Can downvote tips from other users"),
        ]

    def upvoteForUser(self, user):
        if not self.upvote.filter(voted_user=user).exists():
            new_upvote = Upvote(voted_user=user)
            new_upvote.save()
            self.upvote.add(new_upvote)
            self.downvote.filter(voted_user=user).delete()
            self.author.update_reputation()

    def downvoteForUser(self, user):
        if not self.downvote.filter(voted_user=user).exists():
            new_downvote = Downvote(voted_user=user)
            new_downvote.save()
            self.downvote.add(new_downvote)
            self.upvote.filter(voted_user=user).delete()
            self.author.update_reputation()

    def remove_votes(self):
        self.upvote.all().delete()
        self.downvote.all().delete()
        self.author.update_reputation()

    def user_has_upvoted(self, user):
        return self.upvote.filter(voted_user=user).exists()

    def user_has_downvoted(self, user):
        return self.downvote.filter(voted_user=user).exists()

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')} {self.content} by {self.author.username} (rep: {self.author.reputation})"

EOL
echo "✅ MODELS created in $app_models_file."


# Add AUTH_USER_MODEL to the settings.py file of the project.
cat << 'EOL' >> "$settings_file"
AUTH_USER_MODEL = 'ex.CustomUser'  

EOL
echo "✅ AUTH USER MODEL created in $settings_file."


# Create the admin.py file to the app.
cat << 'EOL' >> "$app_admin_file"
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tip, Upvote, Downvote

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Tip)
admin.site.register(Upvote)
admin.site.register(Downvote)

EOL
echo "✅ ADMIN file created in $app_admin_file."


# Create a URL pattern in the urls.py file of the project.
sed -i "1i\\from django.urls.conf import include" "$project_urls_file"

NEW_URL="path('', include('$app_name.urls')),"
sed -i "/urlpatterns = \[/,/]/ s|]|    $NEW_URL\n]|" "$project_urls_file"

echo "✅ URL pattern created in $project_urls_file."


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
from ex.models import CustomUser, Tip
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populates the database with 10 tips from 5 different users'

    def handle(self, *args, **kwargs):
        usernames = ['user1', 'user2', 'user3']
        password = 'pwd'  

        for username in usernames:
            user, created = CustomUser.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'User created: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'User already exists: {username}'))

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
            author = CustomUser.objects.get(username=random.choice(usernames))
            content = tips[i]
            date = timezone.now() - timezone.timedelta(days=random.randint(0, 30))
            
            tip = Tip.objects.create(
                content=content,
                author=author,
                date=date
            )
            
            for _ in range(random.randint(0, 5)):
                tip.upvoteForUser(random.choice(CustomUser.objects.all()))
            
            for _ in range(random.randint(0, 3)):
                tip.downvoteForUser(random.choice(CustomUser.objects.all()))

            self.stdout.write(self.style.SUCCESS(f'Successfully created tip: "{content}" by {author.username}'))

        self.stdout.write(self.style.SUCCESS('Database population completed successfully.'))

EOL
echo "✅ MANAGEMENT COMMAND created to populate the database."


echo -e "\n**********************\n"
