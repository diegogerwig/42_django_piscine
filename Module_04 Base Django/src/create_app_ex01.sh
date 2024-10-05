#!/bin/sh

project_name="d04"
app_name="ex01"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
urls_file="$app_name/urls.py"
project_urls_file="$project_name/urls.py"
templates_dir_app="$app_name/templates/$app_name"
templates_files="../templates/ex01/base.html ../templates/ex01/display.html ../templates/ex01/django.html ../templates/ex01/nav.html ../templates/ex01/templates.html"
static_dir_app="$app_name/static/$app_name"
static_files="../templates/ex01/style1.css ../templates/ex01/style2.css"


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

def django(request):
    return render(request, 'ex01/django.html')

def display(request):
    return render(request, 'ex01/display.html')

def templates(request):
    return render(request, 'ex01/templates.html')
EOL
echo "✅ Views created."


# Create a URL pattern in the urls.py file of the app.
cat <<EOL >> "$urls_file"
from django.urls import path
from . import views

urlpatterns = [
    path('django', views.django, name='django'),
    path('display', views.display, name='display'),
    path('templates', views.templates, name='templates'),
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
]
EOL
echo "✅ URL pattern created in $project_urls_file."


# Create templates in the templates directory of the app.
mkdir -p "$templates_dir_app"
cp $templates_files "$templates_dir_app/"
echo "✅ Templates created in $templates_dir_app."


# Create static files in the static directory of the app.
mkdir -p "$static_dir_app"
cp $static_files "$static_dir_app/"
echo "✅ Static files created in $static_dir_app."
