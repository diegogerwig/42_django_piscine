#!/bin/sh

project_name="d05"
app_name="ex00"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
app_urls_file="$app_name/urls.py"
project_urls_file="$project_name/urls.py"


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
from django.conf import settings
from django.http import HttpRequest, HttpResponse
import psycopg2

def init(request: HttpRequest):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )
        with conn.cursor() as curs:
            curs.execute("""
            CREATE TABLE ex00_movies(
                title VARCHAR(64) UNIQUE NOT NULL,
                episode_nb INT PRIMARY KEY,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL
                );
            """)
            curs.execute('commit')
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(e)
EOL
echo "✅ View created."


# Create a URL pattern in the urls.py file of the app.
cat <<EOL >> "$app_urls_file"
from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init, name='ex00-init'),
]
EOL
echo "✅ URL pattern created in $app_urls_file."


# Create a URL pattern in the urls.py file of the project.
IMPORT_LINE="from django.urls.conf import include"
sed -i "1i\\from django.urls.conf import include" "$project_urls_file"

NEW_URL="path('$app_name/', include('$app_name.urls')),"
sed -i "/urlpatterns = \[/,/]/ s|]|    $NEW_URL\n]|" "$project_urls_file"

echo "✅ URL pattern created in $project_urls_file."


# Create a new database configuration in the settings.py file of the project.
new_db_config="DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'djangotraining',
        'USER': 'djangouser',
        'PASSWORD': 'secret',
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


# Change the timezone to Europe/Madrid in the settings.py file of the project.
sed -i "s/'UTC'/'Europe\/Madrid'/" "$settings_file"
echo "✅ Timezone changed to Europe/Madrid in $settings_file."
