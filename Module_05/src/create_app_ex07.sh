#!/bin/sh

project_name="d05"
app_name="ex07"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
app_urls_file="$app_name/urls.py"
app_forms_file="$app_name/forms.py"
project_urls_file="$project_name/urls.py"
app_models_file="$app_name/models.py"
templates_dir_app="$app_name/templates/$app_name"
templates_files="../templates/$app_name/display.html ../templates/$app_name/remove.html ../templates/$app_name/update.html" 


# Change to the project directory.
cd "$project_name"


# Create a Django app in the project.
python manage.py startapp "$app_name"
echo "✅ $app_name APP created."


# Add the app to the INSTALLED_APPS list in the settings.py file of the project.
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n&/" "$settings_file"
echo "✅ $app_name added to INSTALLED_APPS."


# Create a view in the views.py file of the app.
cat << 'EOL' >> "$views_file"
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db import connection, OperationalError
from .models import Movies
from django.forms import Form
from .forms import UpdateForm
from django.shortcuts import redirect


def table_exists():
    with connection.cursor() as cursor:
        cursor.execute("SELECT to_regclass('ex05_movies');")
        return cursor.fetchone()[0] is not None


def populate(request: HttpRequest):
    temp = ""

    if not table_exists():
        return HttpResponse("❗ The movies table does not exist.")

    movies = [
        {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19"
        },
        {
            "episode_nb": 2,
            "title": "Attack of the Clones",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16"
        },
        {
            "episode_nb": 3,
            "title": "Revenge of the Sith",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19"
        },
        {
            "episode_nb": 4,
            "title": "A New Hope",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25"
        },
        {
            "episode_nb": 5,
            "title": "The Empire Strikes Back",
            "director": "Irvin Kershner",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1980-05-17"
        },
        {
            "episode_nb": 6,
            "title": "Return of the Jedi",
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25"
        },
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11"
        }
    ]

    for item in movies:
        try:
            new_row = Movies(**item)
            new_row.save()
            temp += "✅ OK >> Data inserted successfully. <br>"
        except Exception as e:
            print('Error : ', e)
            temp += f"❌ Error: {item['title']} ::{e} <br>"
    return HttpResponse(temp)


def display(request: HttpRequest):
    response = None
    try:
        response = Movies.objects.all().order_by('episode_nb')
    except Exception as e:
        print('❌ Error : ', e)
        return HttpResponse("❗ No data available")
    if response:
        return render(request, 'ex07/display.html', {'movies': response})
    else:
        return HttpResponse("❗ No data available")


def remove(request: HttpRequest):
    form = Form()
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid() and request.POST['select'][0]:
            Movies.objects.filter(pk=request.POST['select'][0]).delete()
            return redirect('remove') 

    response = Movies.objects.all().order_by('episode_nb')
    if response:
        return render(request, 'ex07/remove.html', {'movies': response, 'form': form})
    else:
        return HttpResponse("❗ No data available")


def update(request: HttpRequest):
    form = UpdateForm()
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid() and request.POST['select'][0]:
            obj = Movies.objects.get(pk=request.POST['select'][0])
            obj.opening_crawl = request.POST['opening_crawl']
            obj.save()

    response = Movies.objects.all().order_by('episode_nb')
    if response:
        return render(request, 'ex07/update.html', {'data': response, 'form': form})
    else:
        return HttpResponse("❗ No data available")
    return HttpResponse("❗ No data available")

EOL
echo "✅ View created."


# Create a URL pattern in the urls.py file of the app.
cat << 'EOL' >> "$app_urls_file"
from django.urls import path
from . import views

urlpatterns = [
    # path('init/', views.init),
    path('populate/', views.populate),
    path('display/', views.display),
    path('remove/', views.remove, name='remove'),
    path('update/', views.update, name='update'),
]
EOL
echo "✅ URL pattern created in $app_urls_file."


# Create the forms.py file to the app.
cat << 'EOL' >> "$app_forms_file"
from django import forms

class RemoveForm(forms.Form):
    title = forms.ChoiceField(choices=(), required=True)

    def __init__(self, choices, *args, **kwargs):
        super(RemoveForm, self).__init__(*args, **kwargs)
        self.fields['title'].choices = choices

class UpdateForm(forms.Form):
    title = forms.ChoiceField(choices=(), required=True)
    opening_crawl = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, choices=None, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        if choices:
            self.fields['title'].choices = choices
EOL
echo "✅ FORMS file created in $app_forms_file."


# Create a URL pattern in the urls.py file of the project.
sed -i "1i\\from django.urls.conf import include" "$project_urls_file"

NEW_URL="path('$app_name/', include('$app_name.urls')),"
sed -i "/urlpatterns = \[/,/]/ s|]|    $NEW_URL\n]|" "$project_urls_file"

echo "✅ URL pattern created in $project_urls_file."


# Add a model to the app.
cat << 'EOL' > "$app_models_file"
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
echo "✅ MODEL created in $app_urls_file."


# Create templates in the templates directory of the app.
mkdir -p "$templates_dir_app"
cp $templates_files "$templates_dir_app/"
echo "✅ Templates created in $templates_dir_app."


echo -e "\n**********************\n"
