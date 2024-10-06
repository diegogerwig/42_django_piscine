import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from ex09.models import Planets, People

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **options):
        try:
            json_file_path = os.path.join(settings.BASE_DIR, 'ex09', 'resources', 'ex09_initial_data.json')
            
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded JSON data'))

            planets_count = 0
            people_count = 0

            for item in data:
                if item['model'] == 'ex09.planets':
                    fields = {k: v if v != '' else None for k, v in item['fields'].items()}
                    Planets.objects.create(**fields)
                    planets_count += 1
                elif item['model'] == 'ex09.people':
                    fields = {k: v if v != '' else None for k, v in item['fields'].items()}
                    homeworld_name = fields.pop('homeworld', None)
                    if homeworld_name:
                        homeworld, _ = Planets.objects.get_or_create(name=homeworld_name)
                        fields['homeworld'] = homeworld
                    People.objects.create(**fields)
                    people_count += 1

            self.stdout.write(self.style.SUCCESS(f'Successfully added {planets_count} planets'))
            self.stdout.write(self.style.SUCCESS(f'Successfully added {people_count} people'))
            self.stdout.write(self.style.SUCCESS('Database population completed successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))

