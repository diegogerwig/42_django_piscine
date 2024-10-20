from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ex.models import Tip
from ex.utils import toggle_vote
from django.utils import timezone
import random

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with 10 tips from 3 different users'

    def handle(self, *args, **kwargs):
        usernames = ['user1', 'user2', 'user3']
        password = 'pwd'  

        for username in usernames:
            user, created = CustomUser.objects.get_or_create(username=username)
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

        for i in range(10):
            author = CustomUser.objects.get(username=random.choice(usernames))
            content = tips[i]
            
            tip = Tip.objects.create(
                content=content,
                author=author
            )
            
            # Simulating upvotes and downvotes
            for _ in range(random.randint(0, 5)):
                voter = random.choice(CustomUser.objects.all())
                toggle_vote(tip, voter, random.choice(['upvote', 'downvote']))

            self.stdout.write(self.style.SUCCESS(f'Successfully created tip: "{content}" by {author.username}'))

        self.stdout.write(self.style.SUCCESS('Database population completed successfully.'))

