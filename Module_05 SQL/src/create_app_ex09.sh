#!/bin/sh

project_name="d05"
app_name="ex09"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
app_urls_file="$app_name/urls.py"
app_forms_file="$app_name/forms.py"
project_urls_file="$project_name/urls.py"
app_models_file="$app_name/models.py"
templates_dir_app="$app_name/templates/$app_name"
templates_files="../templates/$app_name/display.html"
resources_dir_app="$app_name/resources"
resources_files="../resources/ex09/ex09_initial_data.json"
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
from django.http import HttpResponse
from django.db.models import Q
from .models import People, Planets

def display(request):
    try:
        if People.objects.exists() and Planets.objects.exists():
            # Encuentra planetas con 'windy' en su clima
            windy_planets = Planets.objects.filter(
                Q(climate__icontains='windy') | 
                Q(climate__iregex=r'\bwindy\b') |
                Q(climate__icontains='wind')
            )
            
            # Encuentra personas de planetas ventosos
            people = People.objects.filter(homeworld__in=windy_planets).select_related('homeworld').order_by('name')
            
            if people:
                context = {
                    'characters': [
                        {
                            'name': person.name,
                            'homeworld': person.homeworld.name if person.homeworld else 'Unknown',
                            'climate': person.homeworld.climate if person.homeworld else 'Unknown',
                        }
                        for person in people
                    ]
                }
                return render(request, 'ex09/display.html', context)
            else:
                context = {'warning': "No characters found from windy planets."}
                return render(request, 'ex09/display.html', context)
        else:
            return HttpResponse("❗ WARNING >> No data available.<br><br>Follow these steps:<br><br>1.- Stop the Django server.<br><br>2.- Use the following command line to populate the database: python ./d05/manage.py populate_ex09<br><br>3.- Run the Django server: python ./d05/manage.py runserver", status=200)
    except Exception as e:
        return HttpResponse(f"❌ Error: {str(e)}", status=500)

EOL
echo "✅ VIEWS created in $views_file."


# Create a URL pattern in the urls.py file of the app.
cat << 'EOL' >> "$app_urls_file"
from django.urls import path
from . import views

urlpatterns = [
    path('display/', views.display, name='ex09_display'),
]

EOL
echo "✅ URL pattern created in $app_urls_file."


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
from ex09.models import Planets, People

class Command(BaseCommand):
    help = 'Populate the database with data from JSON'

    def handle(self, *args, **options):
        try:
            json_file_path = os.path.join(settings.BASE_DIR, 'ex09', 'resources', 'ex09_initial_data.json')
            
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            Planets.objects.all().delete()
            People.objects.all().delete()

            planets_count = 0
            people_count = 0

            planet_map = {}
            for item in data:
                if item['model'] == 'ex09.planets':
                    planet = Planets.objects.create(
                        id=item['pk'],
                        name=item['fields']['name'],
                        climate=item['fields']['climate'],
                        diameter=item['fields']['diameter'],
                        orbital_period=item['fields']['orbital_period'],
                        population=item['fields']['population'],
                        rotation_period=item['fields']['rotation_period'],
                        surface_water=item['fields']['surface_water'],
                        terrain=item['fields']['terrain'],
                        created=item['fields']['created'],
                        updated=item['fields']['updated']
                    )
                    planet_map[item['pk']] = planet
                    planets_count += 1
                    self.stdout.write(f"Added planet: {planet.name} (Climate: {planet.climate})")

            for item in data:
                if item['model'] == 'ex09.people':
                    homeworld = planet_map.get(item['fields']['homeworld'])
                    person = People.objects.create(
                        id=item['pk'],
                        name=item['fields']['name'],
                        birth_year=item['fields']['birth_year'],
                        gender=item['fields']['gender'],
                        eye_color=item['fields']['eye_color'],
                        hair_color=item['fields']['hair_color'],
                        height=item['fields']['height'],
                        mass=item['fields']['mass'],
                        homeworld=homeworld,
                        created=item['fields']['created'],
                        updated=item['fields']['updated']
                    )
                    people_count += 1
                    self.stdout.write(f"Added person: {person.name} (Homeworld: {person.homeworld.name if person.homeworld else 'Unknown'})")

            self.stdout.write(self.style.SUCCESS(f'Successfully added {planets_count} planets'))
            self.stdout.write(self.style.SUCCESS(f'Successfully added {people_count} people'))
            self.stdout.write(self.style.SUCCESS('Database population completed successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))

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
