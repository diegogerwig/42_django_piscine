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
templates_files="../templates/$app_name/search.html"
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
from django.http import JsonResponse
from .forms import MovieSearchForm
from .models import People, Movies, Planets
# from django.db.models import Q
from datetime import date

def date_handler(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def movie_search(request):
    no_data = not (People.objects.exists() and Movies.objects.exists() and Planets.objects.exists())

    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            request.session['search_data'] = {
                'min_release_date': form.cleaned_data['min_release_date'].isoformat(),
                'max_release_date': form.cleaned_data['max_release_date'].isoformat(),
                'planet_diameter': form.cleaned_data['planet_diameter'],
                'character_gender': form.cleaned_data['character_gender'],
            }
            
            results = perform_search(form.cleaned_data)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'results': results, 'message': "Nothing corresponding to your research" if not results else None}, json_dumps_params={'default': date_handler})
            else:
                return render(request, 'ex10/search.html', {
                    'form': form,
                    'results': results,
                    'message': "Nothing corresponding to your research" if not results else None,
                    'no_data': no_data
                })
    else:
        search_data = request.session.get('search_data')
        if search_data:
            search_data['min_release_date'] = date.fromisoformat(search_data['min_release_date'])
            search_data['max_release_date'] = date.fromisoformat(search_data['max_release_date'])
            form = MovieSearchForm(search_data)
            if form.is_valid():
                results = perform_search(form.cleaned_data)
                return render(request, 'ex10/search.html', {
                    'form': form,
                    'results': results,
                    'message': "Nothing corresponding to your research" if not results else None,
                    'no_data': no_data
                })
        else:
            form = MovieSearchForm()

    return render(request, 'ex10/search.html', {
        'form': form,
        'no_data': no_data
    })

def perform_search(data):
    min_date = data['min_release_date']
    max_date = data['max_release_date']
    planet_diameter = data['planet_diameter']
    gender = data['character_gender']

    people = People.objects.filter(
        homeworld__diameter__gt=planet_diameter,
        movies__release_date__range=[min_date, max_date]
    )
    
    if gender:
        people = people.filter(gender=gender)

    people = people.distinct()

    results = []
    for person in people:
        for movie in person.movies.filter(release_date__range=[min_date, max_date]):
            results.append({
                'movie_title': movie.title,
                'character_name': person.name,
                'gender': person.gender or 'Unknown',
                'homeworld': person.homeworld.name if person.homeworld else 'Unknown',
                'homeworld_diameter': person.homeworld.diameter if person.homeworld else 'Unknown'
            })

    return results

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
from django.core.exceptions import ValidationError
from .models import People

class MovieSearchForm(forms.Form):
    min_release_date = forms.DateField(label='Movies minimum release date')
    max_release_date = forms.DateField(label='Movies maximum release date')
    planet_diameter = forms.IntegerField(label='Planet diameter greater than', min_value=0)
    character_gender = forms.ChoiceField(label='Character gender', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        gender_choices = [('', 'all')]  # 'all' en minúsculas
        gender_choices += [(g.lower(), g.lower()) for g in People.objects.values_list('gender', flat=True).distinct() if g]
        self.fields['character_gender'].choices = gender_choices

    def clean_planet_diameter(self):
        diameter = self.cleaned_data.get('planet_diameter')
        if diameter is not None and diameter < 0:
            raise ValidationError("Planet diameter must be greater than or equal to zero.")
        return diameter

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
    characters = models.ManyToManyField(People, related_name='movies')  # Many-to-many relationship

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

cat << 'EOL' > "$management_dir/populate_ex10.py"
import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
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
                    planets_count = len(planets)

                    # Create people
                    people = {}
                    for item in data:
                        if item['model'] == 'ex10.people':
                            fields = item['fields'].copy()
                            if 'homeworld' in fields and fields['homeworld']:
                                fields['homeworld'] = planets.get(fields['homeworld'])
                            people[item['pk']] = People.objects.create(**fields)
                    people_count = len(people)

                    # Create movies and add characters
                    movies_count = 0
                    for item in data:
                        if item['model'] == 'ex10.movies':
                            fields = item['fields'].copy()
                            characters = fields.pop('characters', [])
                            movie = Movies.objects.create(**fields)
                            movie.characters.set([people[char_id] for char_id in characters if char_id in people])
                            movies_count += 1

                self.stdout.write(self.style.SUCCESS(f'Successfully added {planets_count} planets'))
                self.stdout.write(self.style.SUCCESS(f'Successfully added {people_count} people'))
                self.stdout.write(self.style.SUCCESS(f'Successfully added {movies_count} movies'))
                self.stdout.write(self.style.SUCCESS('Database population completed successfully'))
            
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
