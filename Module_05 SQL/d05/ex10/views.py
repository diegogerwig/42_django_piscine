from django.shortcuts import render

# Create your views here.
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

