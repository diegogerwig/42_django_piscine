import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from ex09.models import Planets, People

class Command(BaseCommand):
    help = 'Populate the database with data from JSON'

    def handle(self, *args, **options):
        try:
            json_file_path = os.path.join(settings.BASE_DIR, 'ex09', 'resources', 'ex09_initial_data.json')
            
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            # Limpiar datos existentes
            Planets.objects.all().delete()
            People.objects.all().delete()

            planets_count = 0
            people_count = 0

            planet_map = {}
            for item in data:
                if item['model'] == 'ex09.planets':
                    planet = Planets.objects.create(
                        id=item['pk'],
                        name=item['fields']['name'],
                        climate=item['fields']['climate'],
                        diameter=item['fields']['diameter'],
                        orbital_period=item['fields']['orbital_period'],
                        population=item['fields']['population'],
                        rotation_period=item['fields']['rotation_period'],
                        surface_water=item['fields']['surface_water'],
                        terrain=item['fields']['terrain'],
                        created=item['fields']['created'],
                        updated=item['fields']['updated']
                    )
                    planet_map[item['pk']] = planet
                    planets_count += 1
                    self.stdout.write(f"Added planet: {planet.name} (Climate: {planet.climate})")

            for item in data:
                if item['model'] == 'ex09.people':
                    homeworld = planet_map.get(item['fields']['homeworld'])
                    person = People.objects.create(
                        id=item['pk'],
                        name=item['fields']['name'],
                        birth_year=item['fields']['birth_year'],
                        gender=item['fields']['gender'],
                        eye_color=item['fields']['eye_color'],
                        hair_color=item['fields']['hair_color'],
                        height=item['fields']['height'],
                        mass=item['fields']['mass'],
                        homeworld=homeworld,
                        created=item['fields']['created'],
                        updated=item['fields']['updated']
                    )
                    people_count += 1
                    self.stdout.write(f"Added person: {person.name} (Homeworld: {person.homeworld.name if person.homeworld else 'Unknown'})")

            self.stdout.write(self.style.SUCCESS(f'Successfully added {planets_count} planets'))
            self.stdout.write(self.style.SUCCESS(f'Successfully added {people_count} people'))
            self.stdout.write(self.style.SUCCESS('Database population completed successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))

