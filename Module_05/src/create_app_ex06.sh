#!/bin/sh

project_name="d05"
app_name="ex06"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
app_urls_file="$app_name/urls.py"
app_forms_file="$app_name/forms.py"
project_urls_file="$project_name/urls.py"
templates_dir_app="$app_name/templates/$app_name"
templates_files="../templates/$app_name/display.html ../templates/$app_name/remove.html ../templates/$app_name/update.html" 


# Change to the project directory.
cd "$project_name"


# Create a Django app in the project.
python manage.py startapp "$app_name"
echo "✅ $app_name APP created."


# Add the app to the INSTALLED_APPS list in the settings.py file of the project.
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n&/" "$settings_file"
echo "✅ $app_name added to INSTALLED_APPS."


# Create a view in the views.py file of the app.
cat << EOL >> "$views_file"
from django.conf import settings
from django.http import HttpRequest, HttpResponse
import psycopg2
from django.shortcuts import render
from django.forms import Form
from .forms import UpdateForm
from django.shortcuts import redirect


TABLE_NAME = "ex06_movies"

def create_table(conn, tablename, content):
    sql_string = "(\n"
    i = 0
    curr = conn.cursor()
    for key, value in content.items():
        i += 1
        if i < len(content):
            sql_string += "    %s %s,\n" % (key, value)
        else:
            sql_string += "    %s %s\n" % (key, value)
    sql_string += ")"
    curr.execute("""CREATE TABLE %s %s""" % (tablename, sql_string))
    conn.commit()
    return conn


def init(request: HttpRequest):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )

        with conn.cursor() as curs:
            try:
                create_table(conn, 'ex06_movies', {
                    'title': 'varchar(64) UNIQUE NOT NULL',
                    'episode_nb': 'int PRIMARY KEY',
                    'opening_crawl': 'text',
                    'director': 'varchar(32) NOT NULL',
                    'producer': 'varchar(128) NOT NULL',
                    'release_date': 'date NOT NULL',
                    'created': 'timestamp NOT NULL DEFAULT NOW()',
                    'updated': 'timestamp NOT NULL DEFAULT NOW()'
                })
            
                curr = conn.cursor()
                curr.execute("""
                    CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                    RETURNS TRIGGER AS $$
                    BEGIN
                    NEW.updated = now();
                    NEW.created = OLD.created;
                    RETURN NEW;
                    END;
                    $$ language 'plpgsql';
                    CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
                    ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
                    update_changetimestamp_column();
                    """)
                conn.commit()
                return HttpResponse("✅ OK >> Table created successfully.")

            except psycopg2.errors.DuplicateTable:
                return HttpResponse("✅ OK >> Table already exists.")
            
            except psycopg2.Error as e:
                conn.rollback()
                return HttpResponse(f"❌ Database error: {e}")
    
    except Exception as e:
        return HttpResponse(f"❌ An error occurred: {e}")


def populate(request: HttpRequest):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )

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

        INSERT_DATA = """
            INSERT INTO {table_name}
            (
                episode_nb,
                title,
                director,
                producer,
                release_date
            )
            VALUES
            (
                %s, %s, %s, %s, %s
            );
            """.format(table_name=TABLE_NAME)

        result = []

        with conn.cursor() as curs:
            for movie in movies:
                try:
                    curs.execute(INSERT_DATA, [
                        movie['episode_nb'],
                        movie['title'],
                        movie['director'],
                        movie['producer'],
                        movie['release_date'],
                    ])
                    result.append("✅ OK >> Data inserted successfully.")
                    conn.commit()
                except psycopg2.errors.UndefinedTable as e:
                    conn.rollback()
                    return HttpResponse("❗ The table does not exist. Please create the table first.")
                except psycopg2.DatabaseError as e:
                    conn.rollback()
                    result.append(e)
        
        return HttpResponse("<br>".join(str(i) for i in result))
    
    except Exception as e:
        return HttpResponse(f"❌ An error occurred: {e}")


def display(request: HttpRequest):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )
        SELECT_TABLE = """
            SELECT * FROM {table_name};
            """.format(table_name=TABLE_NAME)
        with conn.cursor() as curs:
            curs.execute(SELECT_TABLE)
            movies = curs.fetchall()
        if movies:
            return render(request, 'ex06/display.html', {"movies": movies})
        else:
            return HttpResponse("❗ No data available")
    
    except Exception as e:
        return HttpResponse("❗ No data available")


def remove_row(conn, tablename, key, value):
    try:
        with conn.cursor() as curr:
            curr.execute(f"DELETE FROM {tablename} WHERE {tablename}.{key} = %s;", [value])
        conn.commit()
    except Exception as e:
        print('❌ Error : ', e)
    return conn


def remove(request: HttpRequest):
    response = None
    form = Form()
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )

        if request.method == 'POST':
            form = Form(request.POST)
            if form.is_valid() and request.POST.get('select'):
                remove_row(conn, 'ex06_movies', 'episode_nb', request.POST['select'])
                return redirect('remove') 

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT episode_nb, title, opening_crawl, director, producer, release_date
                FROM ex06_movies
                ORDER BY episode_nb;
            """)
            response = cursor.fetchall()

    except psycopg2.Error as e:
        print('❌ Error : ', e)
        return HttpResponse("❗ No data available")

    finally:
        if conn and not conn.closed:
            conn.close()

    if response:
        return render(request, 'ex06/remove.html', {'movies': response, 'form': form})
    else:
        return HttpResponse("❗ No data available")


def update(request: HttpRequest):
    form = UpdateForm()
    conn = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            try:
                cursor.execute("""
                    UPDATE ex06_movies 
                    SET opening_crawl = '%s' 
                    WHERE episode_nb = %s;
                    """ % (
                        request.POST['opening_crawl'],
                        request.POST['select'][0]
                        )
                    )
                conn.commit()
                return redirect('update') 
            except Exception as e:
                print(e)
                conn.rollback()
    try:
        cursor.execute("""
            SELECT episode_nb, title, opening_crawl, director, producer, release_date
            FROM ex06_movies
            ORDER BY episode_nb
            """)
    except Exception as e:
        return HttpResponse("❗ No data available")
    response = cursor.fetchall()
    if response:
        return render(request, 'ex06/update.html', {'movies': response, 'form': form})
    else:
        return HttpResponse("❗ No data available")

EOL
echo "✅ View created."


# Create a URL pattern in the urls.py file of the app.
cat << EOL >> "$app_urls_file"
from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init),
    path('populate/', views.populate),
    path('display/', views.display),
    path('remove/', views.remove, name='remove'),
    path('update/', views.update, name='update'),
]
EOL
echo "✅ URL pattern created in $app_urls_file."


# Create the forms.py file to the app.
cat << EOL >> "$app_forms_file"
from django import forms

class UpdateForm(forms.Form):
    opening_crawl = forms.CharField(required=True)
EOL
echo "✅ FORMS file created in $app_forms_file."


# Create a URL pattern in the urls.py file of the project.
sed -i "1i\\from django.urls.conf import include" "$project_urls_file"

NEW_URL="path('$app_name/', include('$app_name.urls')),"
sed -i "/urlpatterns = \[/,/]/ s|]|    $NEW_URL\n]|" "$project_urls_file"

echo "✅ URL pattern created in $project_urls_file."


# Create templates in the templates directory of the app.
mkdir -p "$templates_dir_app"
cp $templates_files "$templates_dir_app/"
echo "✅ Templates created in $templates_dir_app."


echo -e "\n**********************\n"
