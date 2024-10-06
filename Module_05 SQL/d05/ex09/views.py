from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.db.models import Q
# from .models import People, Planets

# def display(request):
#     # Find all planets and their climates for debugging
#     all_planets = Planets.objects.all()
#     climate_debug = [f"{planet.name}: {planet.climate}" for planet in all_planets]

#     # Find planets with 'windy' or 'wind' in their climate description
#     windy_planets = Planets.objects.filter(
#         Q(climate__icontains='windy') |
#         Q(climate__icontains='wind') |
#         Q(climate__iregex=r'\bwindy\b') |
#         Q(climate__iregex=r'\bwind\b')
#     )

#     # Find all characters, but mark those from windy planets
#     all_characters = People.objects.all().order_by('name')
#     characters = [
#         {
#             'name': char.name,
#             'homeworld': char.homeworld.name if char.homeworld else 'Unknown',
#             'climate': char.homeworld.climate if char.homeworld else 'Unknown',
#             'is_windy': char.homeworld in windy_planets if char.homeworld else False
#         }
#         for char in all_characters
#     ]

#     context = {
#         'characters': characters,
#         'windy_planets': windy_planets,
#         'climate_debug': climate_debug,
#     }
    
#     if all_planets.exists():
#         if not windy_planets.exists():
#             context['warning'] = "Warning: No planets with 'windy' or 'wind' in their climate description found."
#         return render(request, 'ex09/display.html', context)
#     else:
#         debug_info = "<br>".join([
#             f"Total planets: {all_planets.count()}",
#             f"Windy planets: {windy_planets.count()}",
#             f"Characters: {len(characters)}",
#             "Climate data:",
#             *climate_debug,
#             "Character data:",
#             *[f"{char['name']}: {char['homeworld']} ({char['climate']})" for char in characters]
#         ])
#         command = "python ./d05/manage.py populate_ex09"
#         return HttpResponse(f"❗ WARNING >> No data available. Debug info:<br>{debug_info}<br><br>Please use the following command line to populate the database:<br>{command}<br><br>After that run:<br>python ./d05/manage.py runserver", status=200)



from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import People, Planets

def display(request):
    # Find planets with 'windy' in their climate description
    windy_planets = Planets.objects.filter(
        Q(climate__icontains='windy') |
        Q(climate__iregex=r'\bwindy\b')
    )

    # Find characters from windy planets
    characters = People.objects.filter(homeworld__in=windy_planets).order_by('name')
    
    context = {
        'characters': [
            {
                'name': char.name,
                'homeworld': char.homeworld.name if char.homeworld else 'Unknown',
                'climate': char.homeworld.climate if char.homeworld else 'Unknown',
            }
            for char in characters
        ],
    }
    
    if Planets.objects.exists():
        if not windy_planets.exists():
            context['warning'] = "No planets with 'windy' in their climate description found."
        return render(request, 'ex09/display.html', context)
    else:
        command = "python ./d05/manage.py populate_ex09"
        return HttpResponse(f"❗ WARNING >> No data available.<br><br>Please use the following command line to populate the database:<br>{command}<br><br>After that run:<br>python ./d05/manage.py runserver", status=200)











# from django.shortcuts import render
# from django.http import HttpResponse
# from django.db.models import Q
# from .models import People, Planets

# def display(request):
#     # Find all planets and their climates for debugging
#     all_planets = Planets.objects.all()
#     climate_debug = [f"{planet.name}: {planet.climate}" for planet in all_planets]

#     # Find planets with 'windy' or 'wind' in their climate description
#     windy_planets = Planets.objects.filter(
#         Q(climate__icontains='windy') |
#         Q(climate__icontains='wind') |
#         Q(climate__iregex=r'\bwindy\b') |
#         Q(climate__iregex=r'\bwind\b')
#     )

#     # Find all characters, but mark those from windy planets
#     all_characters = People.objects.all().order_by('name')
#     characters = [
#         {
#             'name': char.name,
#             'homeworld': char.homeworld.name if char.homeworld else 'Unknown',
#             'climate': char.homeworld.climate if char.homeworld else 'Unknown',
#             # 'is_windy': char.homeworld in windy_planets if char.homeworld else False
#         }
#         for char in all_characters
#     ]

#     context = {
#         'characters': characters,
#         # 'windy_planets': windy_planets,
#         # 'climate_debug': climate_debug,
#     }
    
#     if all_planets.exists():
#         if not windy_planets.exists():
#             context['warning'] = "❗ WARNING >> No planets with 'windy' or 'wind' in their climate description found."
#         return render(request, 'ex09/display.html', context)
#     else:
#         debug_info = "<br>".join([
#             f"Total planets: {all_planets.count()}",
#             f"Windy planets: {windy_planets.count()}",
#             f"Characters: {len(characters)}",
#             "Climate data:",
#             *climate_debug,
#             "Character data:",
#             *[f"{char['name']}: {char['homeworld']} ({char['climate']})" for char in characters]
#         ])
#         command = "python ./d05/manage.py populate_ex09"
#         return HttpResponse(f"❗ WARNING >> No data available. Debug info:<br>{debug_info}<br><br>Please use the following command line to populate the database:<br>{command}<br><br>After that run:<br>python ./d05/manage.py runserver", status=200)

