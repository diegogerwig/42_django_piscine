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
templates_files="../templates/$app_name/base.html  ../templates/$app_name/nav.html ../templates/$app_name/index.html ../templates/$app_name/login.html ../templates/$app_name/signup.html"


# Change to the project directory.
cd "$project_name"


# Create a Django app in the project.
python manage.py startapp "$app_name"
echo "✅ $app_name APP created."


# Add the app to the INSTALLED_APPS list in the settings.py file of the project.
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n    'django_bootstrap5',\n&/" "$settings_file"
echo "✅ $app_name added to INSTALLED_APPS."


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


# settings for my app
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
echo "✅ BOOTSTRAP CONFIG created in $settings_file."


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
                        id=request.POST['tipid'])).get('auteur') ==
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
                tip.auteur = request.user.username if request.user.is_authenticated else current_user
                tip.save()
                return redirect('home')
    else:
        form = TipForm()
    
    tips = Tip.objects.all().order_by('-date')
    for tip in tips:
        tip.formatted_date = tip.date.strftime('%Y-%m-%d %H:%M:%S')
    
    context = {
        'usador': current_user,
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
                form.add_error(None, 'Unknown or inactive user')
    else:
        form = LoginForm()
    return render(request, 'ex/login.html', {
        'usador': get_current_user(request),
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
    return render(request, 'ex/signup.html', {
        'usador': get_current_user(request),
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
    path('', views.home),
    path('login/', views.login),
	path('signup/', views.signup),
	path('logout/', views.logout),
]

EOL
echo "✅ URL pattern created in $app_urls_file."


# Create the forms.py file to the app.
cat << 'EOL' >> "$app_forms_file"
from django import forms
from django.contrib.auth.models import User
from .models import Tip

class SignupForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput, initial='')
	verif_password = forms.CharField(required=True, widget=forms.PasswordInput, initial='')
	def clean(self):
		form_data = super(SignupForm, self).clean()
		u = User.objects.filter(username=form_data['username'])
		if len(u) > 0:
			self._errors['username'] = ["The name entered is already taken"]
		if form_data['password'] != form_data['verif_password']:
			self._errors['password'] = ["The password must be identical in the 2 password fields"]
		return form_data


class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput, initial='')


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
from django.contrib.auth.models import User
from django.utils import timezone


class Upvote(models.Model):
    voted_user = models.CharField(max_length=150)


class Downvote(models.Model):
    voted_user = models.CharField(max_length=150)


class Tip(models.Model):
    content = models.TextField()
    auteur = models.CharField(max_length=150)
    date = models.DateTimeField(default=timezone.now)
    upvote = models.ManyToManyField(Upvote)
    downvote = models.ManyToManyField(Downvote)

    def upvoteForUser(self, username):
        votes = self.upvote.all()
        found = False
        for index in votes:
            if index.voted_user == username:
                found = True
                index.delete()
                break
        if not found:
            newvote = Upvote(voted_user=username)
            newvote.save()
            self.upvote.add(newvote)

            downvotes = self.downvote.all()
            for index in downvotes:
                if index.voted_user == username:
                    index.delete()
                    break
            self.save()

    def downvoteForUser(self, username):
        votes = self.downvote.all()
        found = False
        for index in votes:
            if index.voted_user == username:
                found = True
                index.delete()
                break
        if not found:
            newvote = Downvote(voted_user=username)
            newvote.save()
            self.downvote.add(newvote)

            upvotes = self.upvote.all()
            for index in upvotes:
                if index.voted_user == username:
                    index.delete()
                    break
            self.save()

    def __str__(self):
        return str(self.date.strftime('%Y-%m-%d %H:%M:%S')) + ' ' + self.content + ' by ' + self.auteur \
               + ' upvotes : ' + str(len(self.upvote.all())) \
               + ' downvotes : ' + str(len(self.downvote.all()))

    def get_auteur(self):
        return self.auteur


EOL
echo "✅ MODELS created in $app_models_file."


# Create a URL pattern in the urls.py file of the project.
sed -i "1i\\from django.urls.conf import include" "$project_urls_file"

NEW_URL="path('', include('$app_name.urls')),"
sed -i "/urlpatterns = \[/,/]/ s|]|    $NEW_URL\n]|" "$project_urls_file"

echo "✅ URL pattern created in $project_urls_file."



# Create templates in the templates directory of the app.
mkdir -p "$templates_dir_app"
cp $templates_files "$templates_dir_app/"
echo "✅ TEMPLATES created in $templates_dir_app."


echo -e "\n**********************\n"
