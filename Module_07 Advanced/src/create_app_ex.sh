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
app_tests_file="$app_name/tests.py"



# Change to the project directory.
cd "$project_name"



# Create a Django app in the project.
python manage.py startapp "$app_name"
echo "✅ <$app_name> APP created."



# Add the app to the INSTALLED_APPS list in the settings.py file of the project.
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    'django_bootstrap5',\n    '$app_name',\n&/" "$settings_file"
echo "✅ <$app_name> added to INSTALLED_APPS."



# Add 'localhost' & '127.0.0.1' to the ALLOWED_HOSTS list in the settings.py file of the project.
sed -i "s/ALLOWED_HOSTS = \[.*\]/ALLOWED_HOSTS = ['localhost', '127.0.0.1']/" "$settings_file"
echo "✅ <localhost> and <127.0.0.1> added to ALLOWED_HOSTS."



# Create a URL pattern in the urls.py file of the project.
sed -i '/from django.urls.conf import include/d' "$project_urls_file"
sed -i 's/from django.urls import path/from django.urls import path, include/' "$project_urls_file"
cat << 'EOL' > "$project_urls_file"
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/articles/', permanent=False)),
    path('i18n/', include('django.conf.urls.i18n')),
    path('articles/', include('ex.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('articles/', include('ex.urls')),
    prefix_default_language=True
)
EOL
echo "✅ URL pattern created in $project_urls_file"



# Create a URL pattern in the urls.py file of the app.
cat << 'EOL' >> "$app_urls_file"
from django.urls import path
from .views import Login, Logout, Register, ArticlesView, Detail, Publish, Publications, Favourite

urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
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
i18n_middleware=$(cat << 'EOL'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ex.middleware.LoginFormMiddleware',
    'ex.middleware.RedirectToArticlesMiddleware'
]
EOL
)



# Replace the entire MIDDLEWARE section in settings.py
awk -v replacement="$i18n_middleware" '
    /^MIDDLEWARE = \[/,/\]/ {
        if (!printed) {
            print replacement
            printed = 1
        }
        next
    }
    { print }
' "$settings_file" > temp_settings && mv temp_settings "$settings_file"
echo "✅ Middlewares updated in settings.py"



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

# Internationalization settings
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True

LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
EOL
echo "✅ BOOTSTRAP5 and i18n CONFIG created in $settings_file."

# Create locale directories
mkdir -p "locale/es/LC_MESSAGES"
mkdir -p "locale/en/LC_MESSAGES"
echo "✅ Locale directories created"

# Create Spanish translation file
cat << 'EOL' > "locale/es/LC_MESSAGES/django.po"
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2024-03-16 12:00+0000\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"Language: es\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"

msgid "ARTICLES"
msgstr "ARTICULOS"

msgid "TITLE"
msgstr "TÍTULO"

msgid "AUTHOR"
msgstr "AUTOR"

msgid "SYNOPSIS"
msgstr "SINOPSIS"

msgid "CREATED"
msgstr "CREADO"

msgid "DETAIL"
msgstr "DETALLES"
EOL
echo "✅ Spanish translations file created"



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
            # Skip if file doesn't exist (in case of no matches)
            [ -e "$file" ] || continue
            
            # Skip __pycache__ directories
            if [[ $(basename "$file") == "__pycache__" ]]; then
                continue
            fi
            
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
                mkdir -p "$dest_dir/$dirname"
                
                if rsync -a --exclude='__pycache__' "$file/" "$dest_dir/$dirname/"; then
                    echo "   📂 Copied directory: $dirname"
                    for subfile in "$file"/*; do
                        [ -e "$subfile" ] || continue
                        if [ -f "$subfile" ] && [[ $(basename "$(dirname "$subfile")") != "__pycache__" ]]; then
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



# Generate message files
python manage.py makemessages -l es
python manage.py makemessages -l en
echo "✅ Language message files created"



# Compile messages
python manage.py compilemessages
echo "✅ Language messages compiled"



# Create tests.py file
cat << 'EOL' > "$app_tests_file"
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, UserFavoriteArticle
from django.contrib.messages import get_messages

class ArticleAccessTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123',
            email='test2@example.com'
        )

    def setUp(self):
        self.client = Client()
        self.article = Article.objects.create(
            title='Test Article',
            author=self.user,
            synopsis='Test Synopsis',
            content='Test Content'
        )

    def test_protected_views_redirect_anonymous_users(self):
        """Test that anonymous users are redirected to login when accessing protected views"""
        protected_urls = [
            reverse('favourite'),
            reverse('publications'),
            reverse('publish'),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('login', response.url)

    def test_protected_views_accessible_to_logged_users(self):
        """Test that logged-in users can access protected views"""
        self.assertTrue(
            self.client.login(username='testuser', password='testpass123')
        )
        
        protected_urls = [
            reverse('favourite'),
            reverse('publications'),
            reverse('publish'),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_register_view_inaccessible_to_logged_users(self):
        """Test that logged-in users cannot access the registration page"""
        self.assertTrue(
            self.client.login(username='testuser', password='testpass123')
        )
        
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('articles'))

    def test_prevent_duplicate_favorites(self):
        """Test that users cannot add the same article to favorites twice"""
        self.assertTrue(
            self.client.login(username='testuser2', password='testpass123')
        )
        
        # First attempt should succeed
        response = self.client.post(reverse('favourite'), {
            'article_id': self.article.id
        })
        self.assertEqual(response.status_code, 302)
        
        self.assertTrue(
            UserFavoriteArticle.objects.filter(
                user=self.user2,
                article=self.article
            ).exists()
        )
        
        # Second attempt should fail
        response = self.client.post(reverse('favourite'), {
            'article_id': self.article.id
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify only one favorite entry exists
        favorite_count = UserFavoriteArticle.objects.filter(
            user=self.user2,
            article=self.article
        ).count()
        self.assertEqual(favorite_count, 1)

    def test_templates_protection(self):
        """Test that protected templates are only accessible to logged-in users"""
        protected_urls = {
            'favourite': reverse('favourite'),
            'publications': reverse('publications'),
            'publish': reverse('publish')
        }

        # Test anonymous access
        for name, url in protected_urls.items():
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 
                302, 
                f"{name} should redirect anonymous users"
            )
            self.assertIn('login', response.url)

        # Test authenticated access
        self.assertTrue(
            self.client.login(username='testuser', password='testpass123')
        )
        for name, url in protected_urls.items():
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 
                200, 
                f"{name} should be accessible to logged users"
            )
EOL
echo "✅ Tests file created in $app_tests_file"






echo -e "\n**********************\n"