#!/bin/sh

project_name="Django_project"
app_name="helloworld_app"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
urls_file="$app_name/urls.py"
project_urls_file="$project_name/urls.py"


# 1. Create a Django project named Django_project.
django-admin startproject "$project_name"
echo "✅ Django_project created."
cd "$project_name"


# 2. Create a Django app named helloworld_app.
python manage.py startapp "$app_name"
echo "✅ helloworld_app created."


# 3. Add the app to the INSTALLED_APPS list in the settings.py file from Django_project dir.
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n&/" "$settings_file"
echo "✅ $app_name added to INSTALLED_APPS."


# 4. Create a view named hello_world in the views.py file from helloworld_app dir.
cat <<EOL >> "$views_file"
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello World!")
EOL
echo "✅ View hello_world created."


# 5. Create a URL pattern in the urls.py file of the app.
cat <<EOL >> "$urls_file"
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
]
EOL
echo "✅ URL pattern created in $urls_file."


# 6. Create a URL pattern in the urls.py file of the project.
cat <<EOL > "$project_urls_file"
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('helloworld/', include('$app_name.urls')),
]
EOL
echo "✅ URL pattern created in $project_urls_file."


# 7. Migrate the changes
python manage.py migrate
echo "✅ Migrated changes."


# 8. Run the server
echo "✅ Running server..."
python manage.py runserver