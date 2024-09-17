#!/bin/sh

project_name="d04"
app_name="ex02"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
urls_file="$app_name/urls.py"
project_urls_file="$project_name/urls.py"
templates_dir_app="$app_name/templates/$app_name"
templates_files="../templates/ex02/base.html  ../templates/ex02/index.html"
# static_dir_app="$app_name/static/$app_name"
# static_files="../templates/ex02/style.css"


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
from django.shortcuts import redirect, render
from django.conf import settings
from . import forms


def index(request: HttpRequest):
    logger = logging.getLogger('history')

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
    history = forms.CharField(label='history')
EOL


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


# Create a temporary file to store the logging configuration
TMP_FILE=$(mktemp)

# Write the logging configuration to the temporary file
cat << EOF > "$TMP_FILE"

# Logging configuration
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_LOG_FILE = os.path.join(BASE_DIR, 'ex02', 'logs.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'history_format': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{asctime}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'history_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': HISTORY_LOG_FILE,
            'mode': 'a',
            'formatter': 'history_format',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'history': {
            'handlers': ['console', 'history_handler'],
            'level': 'INFO'
        }
    }
}
EOF

# Append the contents of the temporary file to settings.py
cat "$TMP_FILE" >> "$settings_file"

# Remove the temporary file
rm "$TMP_FILE"

echo "✅ Logging configuration has been added to $settings_file."


# Change the timezone to Europe/Madrid in the settings.py file of the project.
sed -i "s/'UTC'/'Europe\/Madrid'/" "$settings_file"
echo "✅ Timezone changed to Europe/Madrid in $settings_file."



# Create templates in the templates directory of the app.
mkdir -p "$templates_dir_app"
cp $templates_files "$templates_dir_app/"
echo "✅ Templates created in $templates_dir_app."


# # Create static files in the static directory of the app.
# mkdir -p "$static_dir_app"
# cp $static_files "$static_dir_app/"
# echo "✅ Static files created in $static_dir_app."
