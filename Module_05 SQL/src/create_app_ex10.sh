#!/bin/sh

project_name="d05"
app_name="ex10"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
app_urls_file="$app_name/urls.py"
app_forms_file="$app_name/forms.py"
project_urls_file="$project_name/urls.py"
app_models_file="$app_name/models.py"
templates_dir_app="$app_name/templates/$app_name"
templates_files="../templates/$app_name/display.html"
resources_dir_app="$app_name/resources"
resources_files="../resources/ex10/ex10_initial_data.json"
management_dir="$app_name/management/commands"


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
from .forms import MovieSearchForm
from .models import People, Movies, Planets

def movie_search(request):
    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            min_date = form.cleaned_data['min_release_date']
            max_date = form.cleaned_data['max_release_date']
            planet_diameter = form.cleaned_data['planet_diameter']
            gender = form.cleaned_data['character_gender']

            results = People.objects.filter(
                gender=gender,
                homeworld__diameter__gt=planet_diameter,
                movies__release_date__range=[min_date, max_date]
            ).distinct()

            if not results:
                message = "Nothing corresponding to your research"
            else:
                message = None

            return render(request, 'ex10/results.html', {
                'results': results,
                'form': form,
                'message': message
            })
    else:
        form = MovieSearchForm()

    return render(request, 'ex10/search.html', {'form': form})

EOL
echo "✅ VIEWS created in $views_file."


# Create a URL pattern in the urls.py file of the app.
cat << 'EOL' >> "$app_urls_file"
from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_search, name='movie_search'),
]

EOL
echo "✅ URL pattern created in $app_urls_file."


# Create the forms.py file to the app.
cat << 'EOL' >> "$app_forms_file"
from django import forms
from .models import People

class MovieSearchForm(forms.Form):
    min_release_date = forms.DateField(label='Movies minimum release date')
    max_release_date = forms.DateField(label='Movies maximum release date')
    planet_diameter = forms.IntegerField(label='Planet diameter greater than')
    character_gender = forms.ChoiceField(label='Character gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        gender_choices = People.objects.values_list('gender', flat=True).distinct()
        self.fields['character_gender'].choices = [(g, g) for g in gender_choices if g]

EOL
echo "✅ FORMS file created in $app_forms_file."


# Create models in the models.py file of the app
cat << 'EOL' > "$app_models_file"
from django.db import models

class Planets(models.Model):
    name = models.CharField(max_length=64, unique=True)
    climate = models.TextField(blank=True, null=True)
    diameter = models.IntegerField(null=True)
    orbital_period = models.IntegerField(null=True)
    population = models.BigIntegerField(null=True)
    rotation_period = models.IntegerField(null=True)
    surface_water = models.FloatField(null=True)
    terrain = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class People(models.Model):
    name = models.CharField(max_length=64, unique=True)
    birth_year = models.CharField(max_length=32, null=True)
    gender = models.CharField(max_length=32, null=True)
    eye_color = models.CharField(max_length=32, null=True)
    hair_color = models.CharField(max_length=32, null=True)
    height = models.IntegerField(null=True)
    mass = models.FloatField(null=True)
    homeworld = models.ForeignKey(Planets, on_delete=models.PROTECT, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Movies(models.Model):
    title = models.CharField(max_length=64, unique=True)
    opening_crawl = models.TextField()
    director = models.CharField(max_length=32)
    producer = models.CharField(max_length=128)
    release_date = models.DateField()
    characters = models.ManyToManyField(People, related_name='movies')

    def __str__(self):
        return self.title

EOL
echo "✅ MODELS created in $app_models_file."


# Create a URL pattern in the urls.py file of the project.
sed -i "1i\\from django.urls.conf import include" "$project_urls_file"

NEW_URL="path('$app_name/', include('$app_name.urls')),"
sed -i "/urlpatterns = \[/,/]/ s|]|    $NEW_URL\n]|" "$project_urls_file"

echo "✅ URL pattern created in $project_urls_file."


# Create a management command to populate the database
mkdir -p "$management_dir"
touch "$management_dir/__init__.py"

cat << 'EOL' > "$management_dir/populate_ex09.py"
import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from ex10.models import Planets, People, Movies

class Command(BaseCommand):
    help = 'Populate the database with data from JSON'

    def handle(self, *args, **options):
        try:
            json_file_path = os.path.join(settings.BASE_DIR, 'ex10', 'resources', 'ex10_initial_data.json')
            
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            try:
                with transaction.atomic():
                    # Clear existing data
                    Planets.objects.all().delete()
                    People.objects.all().delete()
                    Movies.objects.all().delete()

                    # Create planets
                    planets = {item['pk']: Planets.objects.create(**item['fields']) 
                            for item in data if item['model'] == 'ex10.planets'}

                    # Create people
                    people = {}
                    for item in data:
                        if item['model'] == 'ex10.people':
                            fields = item['fields'].copy()
                            if 'homeworld' in fields and fields['homeworld']:
                                fields['homeworld'] = planets.get(fields['homeworld'])
                            people[item['pk']] = People.objects.create(**fields)

                    # Create movies and add characters
                    for item in data:
                        if item['model'] == 'ex10.movies':
                            fields = item['fields'].copy()
                            characters = fields.pop('characters', [])
                            movie = Movies.objects.create(**fields)
                            movie.characters.set([people[char_id] for char_id in characters if char_id in people])

                self.stdout.write(self.style.SUCCESS('Successfully populated the database.'))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('The JSON file does not exist.'))

EOL
echo "✅ MANAGEMENT COMMAND created to populate the database."


# Create templates in the templates directory of the app.
mkdir -p "$templates_dir_app"
cp $templates_files "$templates_dir_app/"
echo "✅ TEMPLATES created in $templates_dir_app."


# Create resources in the resources directory of the app.
mkdir -p "$resources_dir_app"
cp $resources_files "$resources_dir_app/"
echo "✅ RESOURCES created in $resources_dir_app."


echo -e "\n**********************\n"
