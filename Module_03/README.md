## EX02 Wikipedia API

https://www.mediawiki.org/wiki/API:Main_page

https://www.mediawiki.org/w/api.php?action=help&modules=parse

https://github.com/daddyd/dewiki

---
---

## EX03 BeautitfulSoup

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

---
---

## EX04 Virtual Environment

The issue is that when you run a Bash script, each command is executed in a subshell. When the script finishes, the virtual environment you activated gets deactivated because the subshell closes.

To keep the virtual environment active after the script finishes, you need to "source" the script instead of running it normally. Here's how to do that:

Instead of running your script as `bash my_script.sh`, use `source my_script.sh`

This will execute the script in the current shell context, keeping the virtual environment active.

---
---

## EX05 Django Project

### Create a new Django project:

django-admin startproject Django_project
cd Django_project

### Create a new Django app within your project:

python manage.py startapp helloworld_app

### Open the Django_project/settings.py file and add your new app to the INSTALLED_APPS list:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'helloworld_app',  # Add this line
]

### Create a view in the helloworld_app/views.py file:

from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello World!")


### Create a new file helloworld_app/urls.py and add the following content:

from django.urls import path
from . import views

urlpatterns = [
    path('helloworld/', views.hello_world, name='hello_world'),
]

### Open the Django_project/urls.py file and include the URLs from your app:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('helloworld/', include('helloworld_app.urls')),
]

### Migrate the changes

python manage.py migrate

### Run the development server:

python manage.py runserver


🎯 Now, if you visit http://localhost:8000/helloworld/ in your web browser, you should see the text "Hello World!" displayed.
