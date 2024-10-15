from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import psycopg2
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

SQL_COMMANDS = [
    """
    CREATE TABLE IF NOT EXISTS ex08_planets (
        id serial PRIMARY KEY,
        name varchar(64) UNIQUE NOT NULL,
        climate text,
        diameter int,
        orbital_period int,
        population bigint,
        rotation_period int,
        surface_water float,
        terrain varchar(128)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ex08_people (
        id serial PRIMARY KEY,
        name varchar(64) UNIQUE NOT NULL,
        birth_year varchar(32),
        gender varchar(32),
        eye_color varchar(32),
        hair_color varchar(32),
        height int,
        mass float,
        homeworld varchar(64) REFERENCES ex08_planets(name)
    )
    """
]


def execute_sql_commands(cur, commands: List[str]) -> None:
    for command in commands:
        cur.execute(command)


def get_db_connection():
    return psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
    )


def execute_db_operation(operation):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            result = operation(cur)
        conn.commit()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        logger.warning(f"Warning: {error}")
        return None
    finally:
        if conn is not None:
            conn.close()


# def init(request: HttpRequest) -> HttpResponse:
#     def create_tables(cur):
#         try:
#             execute_sql_commands(cur, SQL_COMMANDS)
#             return "✅ OK >> Tables created."
#         except Exception as e:
#             return f"❌ Error creating tables: {str(e)}"

#     result = execute_db_operation(create_tables)
#     return HttpResponse(result if result else "❗ WARNING >> Error creating tables", status=200)


def init(request: HttpRequest) -> HttpResponse:
    def create_tables(cur):
        try:
            cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'ex08_planets')")
            planets_exist = cur.fetchone()[0]
            cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'ex08_people')")
            people_exist = cur.fetchone()[0]
            
            if planets_exist and people_exist:
                return "❗ WARNING >> Tables already exist."
            
            execute_sql_commands(cur, SQL_COMMANDS)
            return "✅ OK >> Tables created."
        except Exception as e:
            return f"❌ Error creating tables: {str(e)}"

    result = execute_db_operation(create_tables)
    return HttpResponse(result, status=200)


# def populate(request: HttpRequest) -> HttpResponse:
#     def insert_data(cur):
#         cols_planets = ('name', 'climate', 'diameter', 'orbital_period', 'population', 'rotation_period',
#                         'surface_water', 'terrain')
#         cols_people = ('name', 'birth_year', 'gender', 'eye_color', 'hair_color', 'height',
#                        'mass', 'homeworld')
        
#         with open('ex08/resources/planets.csv', 'r') as file:
#             cur.copy_from(file, 'ex08_planets', columns=cols_planets, null='NULL')
#         with open('ex08/resources/people.csv', 'r') as file:
#             cur.copy_from(file, 'ex08_people', columns=cols_people, null='NULL')
#         return "✅ OK >> Data inserted successfully."

#     result = execute_db_operation(insert_data)
#     return HttpResponse(result if result else "❗ WARNING >> Error populating tables", status=200)


def populate(request: HttpRequest) -> HttpResponse:
    def insert_data(cur) -> List[str]:
        messages = []
        cols_planets = ('name', 'climate', 'diameter', 'orbital_period', 'population', 'rotation_period',
                        'surface_water', 'terrain')
        cols_people = ('name', 'birth_year', 'gender', 'eye_color', 'hair_color', 'height',
                       'mass', 'homeworld')

        def table_exists(table_name):
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table_name,))
            return cur.fetchone()[0]

        def insert_table_data(file_path, table_name, columns):
            if not table_exists(table_name):
                return f"❗ WARNING: {table_name} does not exist. Please create the table first."
            
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cur.fetchone()[0]
                if count > 0:
                    return f"❗ WARNING >> {table_name} already contains data. Skipping insertion."
                
                with open(file_path, 'r') as file:
                    cur.copy_from(file, table_name, columns=columns, null='NULL')
                return f"✅ OK >> {table_name} created and data inserted successfully."
            except Exception as e:
                return f"❌ Error inserting data into {table_name}: {str(e)}"

        messages.append(insert_table_data('ex08/resources/planets.csv', 'ex08_planets', cols_planets))
        messages.append(insert_table_data('ex08/resources/people.csv', 'ex08_people', cols_people))
        
        return messages

    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            results = insert_data(cur)
        conn.commit()
        return HttpResponse("<br>".join(results))
    except (Exception, psycopg2.DatabaseError) as error:
        logger.warning(f"Warning: {error}")
        return HttpResponse(f"Error: {error}", status=200)
    finally:
        if conn is not None:
            conn.close()

def display(request: HttpRequest) -> HttpResponse:
    def fetch_data(cur) -> List[Tuple]:
        cur.execute("""
            SELECT people.name, people.homeworld, planets.climate  
            FROM ex08_people AS people
            JOIN ex08_planets AS planets ON (people.homeworld = planets.name)
            WHERE planets.climate LIKE '%windy%'
            ORDER BY people.name
        """)
        return cur.fetchall()

    result = execute_db_operation(fetch_data)
    
    if result:
        people = [list(item) for item in result]
        for person in people:
            person[-1] = str(person[-1])
        return render(request, 'ex08/display.html', {'people': people})
    else:
        return HttpResponse('❗ WARNING >> No data available', status=200)

