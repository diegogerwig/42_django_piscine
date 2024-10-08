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




# from django.shortcuts import render
# from django.http import HttpResponse
# from django.db.models import Q
# from .models import People, Planets

# def display(request):
#     # Find planets with 'windy' in their climate description
#     windy_planets = Planets.objects.filter(
#         Q(climate__icontains='windy') |
#         Q(climate__iregex=r'\bwindy\b')
#     )

#     # Find characters from windy planets
#     characters = People.objects.filter(homeworld__in=windy_planets).order_by('name')
    
#     context = {
#         'characters': [
#             {
#                 'name': char.name,
#                 'homeworld': char.homeworld.name if char.homeworld else 'Unknown',
#                 'climate': char.homeworld.climate if char.homeworld else 'Unknown',
#             }
#             for char in characters
#         ],
#     }
    
#     if Planets.objects.exists():
#         if not windy_planets.exists():
#             context['warning'] = "No planets with 'windy' in their climate description found."
#         return render(request, 'ex09/display.html', context)
#     else:
#         command = "python ./d05/manage.py populate_ex09"
#         return HttpResponse(f"❗ WARNING >> No data available.<br><br>Please use the following command line to populate the database:<br>{command}<br><br>After that run:<br>python ./d05/manage.py runserver", status=200)




from django.shortcuts import render
from django.http import HttpResponse

from .models import People, Planets


def display(request):
    try:
        people = People.objects.filter(homeworld__climate__contains='windy')\
                .values('name', 'homeworld__name', 'homeworld__climate')\
                .order_by('name')
    except Exception as exception:
        return HttpResponse(exception)
    return render(request, 'ex09/display.html', {'people': people})




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


# # Create the forms.py file to the app.
# cat << 'EOL' >> "$app_forms_file"
# from django import forms
# from .models import Movies


# class RemoveForm(forms.Form):
#     title = forms.ChoiceField(choices=(), required=True)

#     def __init__(self, choices, *args, **kwargs):
#         super(RemoveForm, self).__init__(*args, **kwargs)
#         self.fields['title'].choices = choices


# class UpdateForm(forms.Form):
#     select = forms.ChoiceField(choices=[], required=True)
#     opening_crawl = forms.CharField(widget=forms.Textarea, required=True)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['select'].choices = [(movie.episode_nb, f"Episode {movie.episode_nb}: {movie.title}") for movie in Movies.objects.all().order_by('episode_nb')]

# EOL
# echo "✅ FORMS file created in $app_forms_file."


# Create models in the models.py file of the app
cat << 'EOL' > "$app_models_file"
# from django.db import models

# class Planets(models.Model):
#     name = models.CharField(max_length=64, unique=True, null=False)
#     climate = models.CharField(max_length=255, null=True, blank=True)
#     diameter = models.IntegerField(null=True, blank=True)
#     orbital_period = models.IntegerField(null=True, blank=True)
#     population = models.BigIntegerField(null=True, blank=True)
#     rotation_period = models.IntegerField(null=True, blank=True)
#     surface_water = models.FloatField(null=True, blank=True)
#     terrain = models.CharField(max_length=255, null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# class People(models.Model):
#     name = models.CharField(max_length=64, null=False)
#     birth_year = models.CharField(max_length=32, null=True, blank=True)
#     gender = models.CharField(max_length=32, null=True, blank=True)
#     eye_color = models.CharField(max_length=32, null=True, blank=True)
#     hair_color = models.CharField(max_length=32, null=True, blank=True)
#     height = models.IntegerField(null=True, blank=True)
#     mass = models.FloatField(null=True, blank=True)
#     homeworld = models.ForeignKey(Planets, on_delete=models.SET_NULL, null=True, to_field='name')
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

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
    homeworld = models.ForeignKey('Planets', on_delete=models.PROTECT, max_length=64, null=True)
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
# import json
# import os
# from django.core.management.base import BaseCommand
# from django.conf import settings
# from ex09.models import Planets, People

# class Command(BaseCommand):
#     help = 'Populate the database with initial data'

#     def handle(self, *args, **options):
#         try:
#             json_file_path = os.path.join(settings.BASE_DIR, 'ex09', 'resources', 'ex09_initial_data.json')
            
#             with open(json_file_path, 'r') as file:
#                 data = json.load(file)

#             self.stdout.write(self.style.SUCCESS(f'Successfully loaded JSON data'))

#             planets_count = 0
#             people_count = 0

#             for item in data:
#                 if item['model'] == 'ex09.planets':
#                     fields = {k: v if v != '' else None for k, v in item['fields'].items()}
#                     Planets.objects.create(**fields)
#                     planets_count += 1
#                 elif item['model'] == 'ex09.people':
#                     fields = {k: v if v != '' else None for k, v in item['fields'].items()}
#                     homeworld_name = fields.pop('homeworld', None)
#                     if homeworld_name:
#                         homeworld, _ = Planets.objects.get_or_create(name=homeworld_name)
#                         fields['homeworld'] = homeworld
#                     People.objects.create(**fields)
#                     people_count += 1

#             self.stdout.write(self.style.SUCCESS(f'Successfully added {planets_count} planets'))
#             self.stdout.write(self.style.SUCCESS(f'Successfully added {people_count} people'))
#             self.stdout.write(self.style.SUCCESS('Database population completed successfully'))

#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
#             import traceback
#             self.stdout.write(self.style.ERROR(traceback.format_exc()))

import json
from django.core.management.base import BaseCommand
from ex09.models import Planets, People

class Command(BaseCommand):
    help = 'Populate the database with data from JSON'

    def handle(self, *args, **options):
        try:
            with open('ex09_initial_data.json', 'r') as file:
                data = json.load(file)

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

            for item in data:
                if item['model'] == 'ex09.people':
                    homeworld = planet_map.get(item['fields']['homeworld'])
                    People.objects.create(
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

            self.stdout.write(self.style.SUCCESS(f'Successfully added {planets_count} planets'))
            self.stdout.write(self.style.SUCCESS(f'Successfully added {people_count} people'))
            self.stdout.write(self.style.SUCCESS('Database population completed successfully'))

            self.stdout.write(self.style.SUCCESS('Successfully populated the database'))

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
