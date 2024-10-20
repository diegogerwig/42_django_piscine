from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ex.models import Tip
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populates the database with 10 tips from 5 different users'

    def handle(self, *args, **kwargs):
        usernames = ['user1', 'user2', 'user3']
        password = 'pwd'  

        for username in usernames:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'User created: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'User already exists: {username}'))

        tips = [
            "Always comment your code.",
            "Use version control systems like Git.",
            "Test your code regularly.",
            "Keep your functions small and focused.",
            "Learn keyboard shortcuts for your IDE.",
            "Automate repetitive tasks.",
            "Write self-documenting code.",
            "Stay updated with the latest technologies.",
            "Collaborate and share knowledge with others.",
            "Take regular breaks to avoid burnout."
        ]

        for i in range(5):
            author = random.choice(usernames)
            content = tips[i]
            date = timezone.now() - timezone.timedelta(days=random.randint(0, 30))
            
            tip = Tip.objects.create(
                content=content,
                author=author,
                date=date
            )
            
            for _ in range(random.randint(0, 5)):
                tip.upvoteForUser(random.choice(usernames))
            
            for _ in range(random.randint(0, 3)):
                tip.downvoteForUser(random.choice(usernames))

            self.stdout.write(self.style.SUCCESS(f'Successfully created tip: "{content}" by {author}'))

        self.stdout.write(self.style.SUCCESS('Database population completed successfully.'))

