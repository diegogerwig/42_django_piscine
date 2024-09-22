#!/bin/sh

project_name="d05"
app_name="ex01"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
app_urls_file="$app_name/urls.py"
project_urls_file="$project_name/urls.py"
app_models_file="$app_name/models.py"


# Change to the project directory.
cd "$project_name"


# Create a Django app in the project.
python manage.py startapp "$app_name"
echo "✅ $app_name created."


# Add the app to the INSTALLED_APPS list in the settings.py file of the project.
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n&/" "$settings_file"
echo "✅ $app_name added to INSTALLED_APPS."


# Create a view in the views.py file of the app.
cat << EOL >> "$views_file"
from django.http import HttpResponse

def init(request):
    if request.method == 'GET':
        return HttpResponse("✅ OK >> Model created successfully")
    return HttpResponse(status=405)

EOL
echo "✅ View created."


# Create a URL pattern in the urls.py file of the app.
cat << EOL >> "$app_urls_file"
from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init, name='ex01'),
]
EOL
echo "✅ URL pattern created in $app_urls_file."


# Create a URL pattern in the urls.py file of the project.
sed -i "1i\\from django.urls.conf import include" "$project_urls_file"

NEW_URL="path('$app_name/', include('$app_name.urls')),"
sed -i "/urlpatterns = \[/,/]/ s|]|    $NEW_URL\n]|" "$project_urls_file"

echo "✅ URL pattern created in $project_urls_file."


# Add a model to the app.
cat << EOL > "$app_models_file"
from django.db import models

class Movies(models.Model):
    title = models.CharField(max_length=64, unique=True, null=False)
    episode_nb = models.IntegerField(primary_key=True)
    opening_crawl = models.TextField(null=True)
    director = models.CharField(max_length=32, null=False)
    producer = models.CharField(max_length=128, null=False)
    release_date = models.DateField(null=False)

    def __str__(self):
        return self.title
EOL
echo "✅ URL pattern created in $app_urls_file."


# Change the timezone to Europe/Madrid in the settings.py file of the project.
sed -i "s/'UTC'/'Europe\/Madrid'/" "$settings_file"
echo "✅ Timezone changed to Europe/Madrid in $settings_file."
