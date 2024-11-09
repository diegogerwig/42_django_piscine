#!/bin/sh

# Directory names
project_name="d09"
app_name="account"



# Project files paths
settings_file="$project_name/settings.py"
project_urls_file="$project_name/urls.py"
app_urls_file="$app_name/urls.py"



# Root level directories (en vez de app level)
templates_dir="templates"
scripts_dir="scripts"



# App directory structure
views_dir_app="$app_name/views"
forms_dir_app="$app_name/forms"
models_dir_app="$app_name/models"
management_dir_app="$app_name/management/commands"



# Source directories (current directory)
views_source_dir="views/account"
forms_source_dir="forms/account"
models_source_dir="models/account"
templates_source_dir="templates/account"
scripts_source_dir="scripts/account"
management_source_dir="management"



# Create Django project and app
cd "$project_name"
python manage.py startapp "$app_name"
echo "✅ <$app_name> APP created."



# Update INSTALLED_APPS
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n    'django_bootstrap5',\n&/" "$settings_file"
echo "✅ Apps added to INSTALLED_APPS."



# Update ALLOWED_HOSTS
sed -i "s/ALLOWED_HOSTS = \[.*\]/ALLOWED_HOSTS = ['localhost', '127.0.0.1']/" "$settings_file"
echo "✅ Allowed hosts updated."



# Update TEMPLATES en settings.py
sed -i "/TEMPLATES = \[/,/]/ s/'DIRS': \[\],/'DIRS': \[BASE_DIR \/ 'templates'\],/" "$settings_file"
echo "✅ Templates directory configured."



# Create project URLs
cat << 'EOL' > "$project_urls_file"
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
import os
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('scripts/<path:path>', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'scripts')
    }),
]
EOL
echo "✅ Project URLs configured."



# Create app URLs (sin la ruta de scripts, ya que está en project_urls)
cat << 'EOL' > "$app_urls_file"
from django.urls import path
from account.views.auth_views import account_view, login_view, logout_view, register_view

urlpatterns = [
    path('account/', account_view, name='account'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]
EOL
echo "✅ App URLs configured."



# Add Bootstrap configuration
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
}
EOL
echo "✅ Bootstrap configuration added."



# Copy files from source to destination directory
copy_directory_contents() {
    local source_dir=$1
    local dest_dir=$2
    local dir_type=$3
    local had_errors=false

    mkdir -p "$dest_dir"
    
    if [ -d "../$source_dir" ]; then
        echo -e "\n📁 Copying $dir_type files from ../$source_dir:"
        
        for file in "../$source_dir"/*; do
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
        echo "❗ $dir_type source directory not found: ../$source_dir"
        return 1
    fi
}



# Create necessary directories at root level
mkdir -p "$templates_dir"
mkdir -p "$scripts_dir"



# Create necessary directories in the app
mkdir -p "$views_dir_app"
mkdir -p "$forms_dir_app"
mkdir -p "$models_dir_app"
mkdir -p "$management_dir_app"



# Create __init__.py files
touch "$views_dir_app/__init__.py"
touch "$forms_dir_app/__init__.py"
touch "$models_dir_app/__init__.py"



# Copy files from source directories
copy_directory_contents "$views_source_dir" "$views_dir_app" "VIEWS"
copy_directory_contents "$forms_source_dir" "$forms_dir_app" "FORMS"
copy_directory_contents "$models_source_dir" "$models_dir_app" "MODELS"
copy_directory_contents "$templates_source_dir" "$templates_dir" "TEMPLATES"
copy_directory_contents "$scripts_source_dir" "$scripts_dir" "SCRIPTS"
copy_directory_contents "$management_source_dir" "$management_dir_app" "MANAGEMENT"



echo -e "\n✨ Setup complete!"