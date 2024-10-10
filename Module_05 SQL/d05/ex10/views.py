from django.shortcuts import render

# Create your views here.
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

