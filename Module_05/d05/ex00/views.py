from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpRequest, HttpResponse
import psycopg2

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
                curs.execute("""
                CREATE TABLE ex00_movies(
                    title VARCHAR(64) UNIQUE NOT NULL,
                    episode_nb INT PRIMARY KEY,
                    opening_crawl TEXT,
                    director VARCHAR(32) NOT NULL,
                    producer VARCHAR(128) NOT NULL,
                    release_date DATE NOT NULL
                );
                """)
                conn.commit()
                return HttpResponse("✅ OK >> Table created successfully.")
            except psycopg2.errors.DuplicateTable:
                return HttpResponse("✅ OK >> Table already exists.")
    except Exception as e:
        return HttpResponse(f"❌ An error occurred: {e}")
