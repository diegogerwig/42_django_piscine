import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from ex10.models import Planets, People, Movies

class Command(BaseCommand):
    help = 'Populate the database with data from JSON'

    def handle(self, *args, **options):
        try:
            json_file_path = os.path.join(settings.BASE_DIR, 'ex10', 'resources', 'ex10_initial_data.json')
            
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            try:
                with transaction.atomic():
                    # Clear existing data
                    Planets.objects.all().delete()
                    People.objects.all().delete()
                    Movies.objects.all().delete()

                    # Create planets
                    planets = {item['pk']: Planets.objects.create(**item['fields']) 
                               for item in data if item['model'] == 'ex10.planets'}
                    planets_count = len(planets)

                    # Create people
                    people = {}
                    for item in data:
                        if item['model'] == 'ex10.people':
                            fields = item['fields'].copy()
                            if 'homeworld' in fields and fields['homeworld']:
                                fields['homeworld'] = planets.get(fields['homeworld'])
                            people[item['pk']] = People.objects.create(**fields)
                    people_count = len(people)

                    # Create movies and add characters
                    movies_count = 0
                    for item in data:
                        if item['model'] == 'ex10.movies':
                            fields = item['fields'].copy()
                            characters = fields.pop('characters', [])
                            movie = Movies.objects.create(**fields)
                            movie.characters.set([people[char_id] for char_id in characters if char_id in people])
                            movies_count += 1

                self.stdout.write(self.style.SUCCESS(f'Successfully added {planets_count} planets'))
                self.stdout.write(self.style.SUCCESS(f'Successfully added {people_count} people'))
                self.stdout.write(self.style.SUCCESS(f'Successfully added {movies_count} movies'))
                self.stdout.write(self.style.SUCCESS('Database population completed successfully'))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('The JSON file does not exist.'))

