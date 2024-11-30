from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat.models.chat_models import UserStatus

class Command(BaseCommand):
    help = 'Create UserStatus for all users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        created_count = 0
        for user in users:
            _, created = UserStatus.objects.get_or_create(user=user)
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {created_count} user statuses'
        ))