#!/bin/sh

project_name="d04"
app_name="ex02"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
urls_file="$app_name/urls.py"
project_urls_file="$project_name/urls.py"
templates_dir_app="$app_name/templates/$app_name"
templates_files="../templates/ex02/base.html  ../templates/ex02/index.html"


# Change to the project directory.
cd "$project_name"


# Create a Django app in the project.
python manage.py startapp "$app_name"
echo "✅ $app_name created."


# Add the app to the INSTALLED_APPS list in the settings.py file of the project.
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n&/" "$settings_file"
echo "✅ $app_name added to INSTALLED_APPS."


# Create a view in the views.py file of the app.
cat <<EOL >> "$views_file"
import logging
from django.http import HttpRequest
from django.shortcuts import redirect
from django.conf import settings
from . import forms


def index(request: HttpRequest):
    logger = logging.getLogger('history' )

    if request.method == 'POST':
        form = forms.History(request.POST)
        if form.is_valid():
            logger.info(form.cleaned_data['history'])
        return redirect('/ex02')
    try:
        f = open(settings.HISTORY_LOG_FILE, 'r')
        historys = [line for line in f.readlines()]
    except:
        historys = []

    return render(request, 'ex02/index.html', {'form': forms.History(), 'historys': historys})
EOL
echo "✅ Views created."


# Create a form in the forms.py file of the app.
cat <<EOL > "$app_name/forms.py"
from django import forms

class History(forms.Form):
    history = forms.CharField(
        label='📝 Your message (max 50 characters)',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Max 50 characters'})
    )

    def clean_history(self):
        data = self.cleaned_data['history']
        if len(data) > 50:
            raise forms.ValidationError("The message is too long.")
        return data
EOL
echo "✅ Form created."


# Create a URL pattern in the urls.py file of the app.
cat <<EOL >> "$urls_file"
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
EOL
echo "✅ URL pattern created in $urls_file."


# Create a URL pattern in the urls.py file of the project.
cat <<EOL > "$project_urls_file"
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ex00/', include('ex00.urls')),
    path('ex01/', include('ex01.urls')),
    path('ex02/', include('ex02.urls')),
]
EOL
echo "✅ URL pattern created in $project_urls_file."


# Add the logging configuration to the settings.py file of the project.

# Ensure the settings file is provided
if [ -z "$settings_file" ]; then
    echo "❌ Error: 'settings_file' not provided."
    exit 1
fi

# Check if settings file exists
if [ ! -f "$settings_file" ]; then
    echo "❌ Error: '$settings_file' not found."
    exit 1
fi

# Append the logging configuration directly to settings.py
cat << EOF >> "$settings_file"
# Logging configuration
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_LOG_FILE = os.path.join(BASE_DIR, 'ex02', 'logs.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[{asctime}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': HISTORY_LOG_FILE,
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'history': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}
EOF
echo "✅ Logging configuration has been added to $settings_file."


# Change the timezone to Europe/Madrid in the settings.py file of the project.
sed -i "s/'UTC'/'Europe\/Madrid'/" "$settings_file"
echo "✅ Timezone changed to Europe/Madrid in $settings_file."


# Create templates in the templates directory of the app.
mkdir -p "$templates_dir_app"
cp $templates_files "$templates_dir_app/"
echo "✅ Templates created in $templates_dir_app."
