#!/bin/bash

project_name="d05"
app_name="ex09"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
app_urls_file="$app_name/urls.py"
project_urls_file="$project_name/urls.py"
app_models_file="$app_name/models.py"
templates_dir_app="$app_name/templates/$app_name"
management_dir="$app_name/management/commands"
initial_data_file="ex09_initial_data.json"

# Change to the project directory
cd "$project_name"

# Create a Django app in the project
python manage.py startapp "$app_name"
echo "✅ $app_name APP created."

# Add the app to the INSTALLED_APPS list in the settings.py file of the project
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n&/" "$settings_file"
echo "✅ $app_name added to INSTALLED_APPS."

# Create models in the models.py file of the app
cat << 'EOL' > "$app_models_file"
from django.db import models
from django.utils import timezone

class Planets(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)
    climate = models.CharField(max_length=255)
    diameter = models.IntegerField()
    orbital_period = models.IntegerField()
    population = models.BigIntegerField()
    rotation_period = models.IntegerField()
    surface_water = models.FloatField()
    terrain = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class People(models.Model):
    name = models.CharField(max_length=64, null=False)
    birth_year = models.CharField(max_length=32)
    gender = models.CharField(max_length=32)
    eye_color = models.CharField(max_length=32)
    hair_color = models.CharField(max_length=32)
    height = models.IntegerField()
    mass = models.FloatField()
    homeworld = models.ForeignKey(Planets, on_delete=models.CASCADE, to_field='name')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

EOL
echo "✅ Models created in $app_models_file."

# Create a view in the views.py file of the app
cat << 'EOL' > "$views_file"
from django.shortcuts import render
from django.http import HttpResponse
from .models import People, Planets

def display(request):
    windy_planets = Planets.objects.filter(climate__icontains='windy')
    characters = People.objects.filter(homeworld__in=windy_planets).order_by('name')
    
    if characters.exists():
        context = {'characters': characters}
        return render(request, 'ex09/display.html', context)
    else:
        command = "python manage.py populate_ex09"
        return HttpResponse(f"No data available, please use the following command line before use:<br>{command}")

EOL
echo "✅ View created."

# Create a URL pattern in the urls.py file of the app
cat << 'EOL' > "$app_urls_file"
from django.urls import path
from . import views

urlpatterns = [
    path('display/', views.display, name='ex09_display'),
]
EOL
echo "✅ URL pattern created in $app_urls_file."

# Create a URL pattern in the urls.py file of the project
sed -i "1i from django.urls import include" "$project_urls_file"
NEW_URL="path('ex09/', include('ex09.urls')),"
sed -i "/urlpatterns = \[/,/]/ s|]|    $NEW_URL\n]|" "$project_urls_file"
echo "✅ URL pattern created in $project_urls_file."

# Create templates in the templates directory of the app
mkdir -p "$templates_dir_app"
cat << 'EOL' > "$templates_dir_app/display.html"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Star Wars Characters</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Star Wars Characters from Windy Planets</h1>
    <table>
        <tr>
            <th>Name</th>
            <th>Homeworld</th>
            <th>Climate</th>
        </tr>
        {% for character in characters %}
        <tr>
            <td>{{ character.name }}</td>
            <td>{{ character.homeworld.name }}</td>
            <td>{{ character.homeworld.climate }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
EOL
echo "✅ Template created in $templates_dir_app/display.html."

# Create a management command to populate the database
mkdir -p "$management_dir"
touch "$management_dir/__init__.py"

cat << 'EOL' > "$management_dir/populate_ex09.py"
import json
from django.core.management.base import BaseCommand
from ex09.models import Planets, People

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        with open('ex09_initial_data.json', 'r') as file:
            data = json.load(file)

        for planet_data in data['planets']:
            Planets.objects.create(**planet_data)

        for people_data in data['people']:
            homeworld = Planets.objects.get(name=people_data['homeworld'])
            People.objects.create(homeworld=homeworld, **{k: v for k, v in people_data.items() if k != 'homeworld'})

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))

EOL
echo "✅ Management command created to populate the database."

echo -e "\n**********************\n"
echo "Setup complete. To populate the database, run:"
echo "python manage.py populate_ex09"
echo -e "\n**********************\n"