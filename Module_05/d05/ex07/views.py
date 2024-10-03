from django.shortcuts import render

# Create your views here.
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

