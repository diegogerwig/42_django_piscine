#!/bin/sh

project_name="d07"
app_name="ex"

settings_file="$project_name/settings.py"
project_urls_file="$project_name/urls.py"
app_urls_file="$app_name/urls.py"

views_dir_app="$app_name/views"
views_source_dir="../views"

forms_dir_app="$app_name/forms"
forms_source_dir="../forms"

models_dir_app="$app_name/models"
models_source_dir="../models"

templates_dir_app="$app_name/templates"
templates_source_dir="../templates"

management_dir_app="$app_name/management/commands"
management_source_dir="../management"

app_admin_file="$app_name/admin.py"
app_utils_file="$app_name/utils.py"



# Change to the project directory.
cd "$project_name"



# Create a Django app in the project.
python manage.py startapp "$app_name"
echo "✅ <$app_name> APP created."



# Add the app to the INSTALLED_APPS list in the settings.py file of the project.
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n    'django_bootstrap5',\n&/" "$settings_file"
echo "✅ <$app_name> added to INSTALLED_APPS."



# Add 'localhost' & '127.0.0.1' to the ALLOWED_HOSTS list in the settings.py file of the project.
sed -i "s/ALLOWED_HOSTS = \[.*\]/ALLOWED_HOSTS = ['localhost', '127.0.0.1']/" "$settings_file"
echo "✅ <localhost> and <127.0.0.1> added to ALLOWED_HOSTS."



# Create a URL pattern in the urls.py file of the project.
sed -i '/from django.urls.conf import include/d' "$project_urls_file"
sed -i 's/from django.urls import path/from django.urls import path, include/' "$project_urls_file"
NEW_URL="path('', include('$app_name.urls')),"
sed -i "/urlpatterns = \[/,/]/ s|]|    $NEW_URL\n]|" "$project_urls_file"
echo "✅ URL pattern created in $project_urls_file."



# Create a URL pattern in the urls.py file of the app.
cat << 'EOL' >> "$app_urls_file"
from django.urls import path
from django.views.generic import RedirectView
from .views import Login, Logout, Register, ArticlesView, Detail, Publish, Publications, Favourite

urlpatterns = [
    path('', RedirectView.as_view(url='articles/', permanent=False), name='index'),
    path('articles/', ArticlesView.as_view(), name='articles'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('articles/<slug:pk>/', Detail.as_view(), name='articles_detail'),
    path('publish/', Publish.as_view(), name='publish'),
    path('publications/', Publications.as_view(), name='publications'),
    path('favourite/', Favourite.as_view(), name='favourite')
]

EOL
echo "✅ URL pattern created in $app_urls_file."



# Create a middleware file in the app.
middleware_file="$app_name/middleware.py"
cat << 'EOL' > "$middleware_file"
from django.shortcuts import redirect
from django.urls import resolve, Resolver404
from django.contrib.auth.forms import AuthenticationForm

class LoginFormMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            request.login_form = AuthenticationForm()
        response = self.get_response(request)
        return response

class RedirectToArticlesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.method == 'POST':
                return self.get_response(request)
            
            resolve(request.path)
            response = self.get_response(request)
            return response
        except Resolver404:
            return redirect('articles')
EOL
echo "✅ Middleware file created with both middlewares in $middleware_file"



# Add the middlewares to the MIDDLEWARE list in the settings.py file of the project.
sed -i "/MIDDLEWARE = \[/a\    '$app_name.middleware.RedirectToArticlesMiddleware'," "$settings_file"
sed -i "/django.contrib.auth.middleware.AuthenticationMiddleware/a\    '$app_name.middleware.LoginFormMiddleware'," "$settings_file"
echo "✅ Middlewares added to MIDDLEWARE in settings.py"



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
    "css_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        "integrity": "sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
        "crossorigin": "anonymous",
    },
    "javascript_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",
        "crossorigin": "anonymous",
    },
    "javascript_in_head": False,
    "horizontal_label_class": "col-sm-3",
    "horizontal_field_class": "col-sm-9",
    "set_placeholder": True,
    "required_css_class": "",
    "error_css_class": "is-invalid",
    "success_css_class": "",  
}

EOL
echo "✅ BOOTSTRAP CONFIG created in $settings_file."



# Function to copy files from source to destination directory
copy_directory_contents() {
    local source_dir=$1
    local dest_dir=$2
    local dir_type=$3
    local had_errors=false

    mkdir -p "$dest_dir"
    
    if [ -d "$source_dir" ]; then
        echo -e "\n📁 Copying $dir_type files from $source_dir:"
        
        for file in "$source_dir"/*; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                if cp "$file" "$dest_dir/"; then
                    echo "   ✅ Copied: $filename"
                else
                    echo "   ❌ Failed to copy: $filename"
                    had_errors=true
                fi
            elif [ -d "$file" ]; then
                dirname=$(basename "$file")
                if cp -r "$file" "$dest_dir/"; then
                    echo "   📂 Copied directory: $dirname"
                    for subfile in "$file"/*; do
                        if [ -f "$subfile" ]; then
                            subfilename=$(basename "$subfile")
                            if [ -f "$dest_dir/$dirname/$subfilename" ]; then
                                echo "      📄 Copied: $dirname/$subfilename"
                            else
                                echo "      ❌ Failed to copy: $dirname/$subfilename"
                                had_errors=true
                            fi
                        fi
                    done
                else
                    echo "   ❌ Failed to copy directory: $dirname"
                    had_errors=true
                fi
            fi
        done
        
        if [ "$had_errors" = true ]; then
            echo "❌ Some $dir_type files failed to copy"
            return 1
        else
            echo "⭐ $dir_type copied successfully to $dest_dir/"
            return 0
        fi
    else
        echo "❗ $dir_type source directory not found: $source_dir"
        return 1
    fi
}

# Copy VIEWS
copy_directory_contents "$views_source_dir" "$views_dir_app" "VIEWS"

# Copy FORMS
copy_directory_contents "$forms_source_dir" "$forms_dir_app" "FORMS"

# Copy MODELS
copy_directory_contents "$models_source_dir" "$models_dir_app" "MODELS"

# Copy TEMPLATES
copy_directory_contents "$templates_source_dir" "$templates_dir_app" "TEMPLATES"

# Copy MANAGEMENT
copy_directory_contents "$management_source_dir" "$management_dir_app" "MANAGEMENT COMMANDS"



# # Create the admin.py file to the app.
# cat << 'EOL' >> "$app_admin_file"

# EOL
# echo "✅ ADMIN file created in $app_admin_file."



# # Create the utils.py file to the app.
# cat << 'EOL' >> "$app_utils_file"

# EOL
# echo "✅ UTILS file created in $app_utils_file."



echo -e "\n**********************\n"
