#!/bin/sh

project_name="d04"
app_name="ex00"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
urls_file="$app_name/urls.py"
project_urls_file="$project_name/urls.py"
templates_dir_app="$app_name/templates/$app_name"
templates_files="templates/index.html"

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
def index(request):
    return render(request, 'ex00/index.html')
EOL
echo "✅ View hello_world created."


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
]
EOL
echo "✅ URL pattern created in $project_urls_file."


# Create a template in the templates directory of the app.
mkdir -p "$templates_dir_app"
cp "$templates_files" "$templates_dir_app"


# Migrate the changes
python manage.py migrate
echo "✅ Migrated changes."


# Run the server
echo "✅ Running server..."
python manage.py runserver