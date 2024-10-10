from django.shortcuts import render

# Create your views here.




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

