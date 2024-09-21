#!/bin/sh

project_name="d04"
app_name="ex03"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
urls_file="$app_name/urls.py"
project_urls_file="$project_name/urls.py"
templates_dir_app="$app_name/templates/$app_name"
templates_files="../templates/ex03/base.html  ../templates/ex03/index.html"


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
from django.shortcuts import render

def index(request):
    total_shades = 50
    increment = 255 / (total_shades - 1)
    
    shades = [
        "{:02X}".format(int(i * increment)) 
        for i in range(total_shades)
    ]

    context = {
        "range": shades
    }

    return render(request, 'ex03/index.html', context)
EOL
echo "✅ Views created."


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
    path('ex03/', include('ex03.urls')),
]
EOL
echo "✅ URL pattern created in $project_urls_file."


# Change the timezone to Europe/Madrid in the settings.py file of the project.
sed -i "s/'UTC'/'Europe\/Madrid'/" "$settings_file"
echo "✅ Timezone changed to Europe/Madrid in $settings_file."


# Create templates in the templates directory of the app.
mkdir -p "$templates_dir_app"
cp $templates_files "$templates_dir_app/"
echo "✅ Templates created in $templates_dir_app."
