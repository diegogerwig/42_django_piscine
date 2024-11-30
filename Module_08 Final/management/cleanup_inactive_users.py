from django.core.management.base import BaseCommand
from django.utils import timezone
from chat.models.chat_models import UserStatus

class Command(BaseCommand):
    help = 'Clean up inactive users'

    def handle(self, *args, **options):
        UserStatus.objects.filter(
            is_online=True,
            last_activity__lt=timezone.now() - timezone.timedelta(minutes=5)
        ).update(is_online=False)
        
        self.stdout.write(self.style.SUCCESS('Successfully cleaned up inactive users'))