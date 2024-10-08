from django.shortcuts import render

# Create your views here.
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
            
                try:
                    curs.execute("""
                        CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                        RETURNS TRIGGER AS $$
                        BEGIN
                            NEW.updated = now();
                            NEW.created = OLD.created;
                            RETURN NEW;
                        END;
                        $$ LANGUAGE plpgsql;

                        CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
                        ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
                        update_changetimestamp_column();
                        """)
                    conn.commit()
                    return HttpResponse("✅ OK >> Table, function, and trigger created successfully.")
                
                except psycopg2.Error as e:
                    conn.rollback()
                    return HttpResponse(f"❌ Error creating function or trigger: {e}")

            except psycopg2.errors.DuplicateTable:
                return HttpResponse("✅ OK >> Table already exists.")
            
            # except psycopg2.Error as e:
            #     conn.rollback()
            #     return HttpResponse(f"❌ Database error: {e}")
    
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
                    result.append(f"❌ Error >> {e}")

        # Si no hay errores, devolvemos los mensajes de éxito
        if all("OK" in res for res in result):
            return HttpResponse("<br>".join(result))
        else:
            # Si hay algunos errores, los mostramos junto con los éxitos
            return HttpResponse("<br>".join(result))
    
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
                return redirect('ex06_remove') 

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
    conn = None
    cursor = None
    
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Fetch movies for choices
        cursor.execute("SELECT episode_nb, title FROM ex06_movies ORDER BY episode_nb")
        choices = [(str(row['episode_nb']), row['title']) for row in cursor.fetchall()]

        if request.method == 'POST':
            form = UpdateForm(choices, request.POST)
            if form.is_valid():
                episode_nb = form.cleaned_data['title']
                opening_crawl = form.cleaned_data['opening_crawl']
                cursor.execute("""
                    UPDATE ex06_movies 
                    SET opening_crawl = %s
                    WHERE episode_nb = %s
                    RETURNING *;
                    """, (opening_crawl, episode_nb))
                updated_row = cursor.fetchone()
                conn.commit()
                return redirect('ex06_update')
        else:
            form = UpdateForm(choices=choices)
        
        cursor.execute("""
            SELECT episode_nb, title, opening_crawl, director, producer, release_date, updated
            FROM ex06_movies
            ORDER BY episode_nb
            """)
        movies = cursor.fetchall()
        
        return render(request, 'ex06/update.html', {'movies': movies, 'form': form})
    
    except Exception as e:
        return HttpResponse(f"❗ An error occurred: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

