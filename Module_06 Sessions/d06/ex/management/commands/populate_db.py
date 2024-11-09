from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ex.models import Tip, CustomGroup
from ex.utils import toggle_vote
from django.utils import timezone
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with superuser, users, group and tips'

    def handle(self, *args, **kwargs):
        admin_username = 'admin'
        admin_password = 'pwd'
        
        User.objects.filter(username=admin_username).delete()
        
        superuser = User.objects.create_superuser(
            username=admin_username,
            password=admin_password,
            email='admin@example.com'
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser created: {admin_username}'))

        CustomGroup.objects.filter(name='Privileged Users').delete()
        
        privileged_group = CustomGroup.objects.create(
            name='Privileged Users',
            manual_can_downvote=True,
            manual_can_delete=True
        )
        self.stdout.write(self.style.SUCCESS(f'Group created: Privileged Users with special permissions'))

        usernames = ['user1', 'user2', 'user3']
        password = 'pwd'

        for username in usernames:
            User.objects.filter(username=username).delete()
            
            user = User.objects.create_user(
                username=username,
                password=password
            )
            user.groups.add(privileged_group)
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f'User created and added to group: {username}'))

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
            author = User.objects.get(username=random.choice(usernames))
            content = tips[i]
            
            tip = Tip.objects.create(
                content=content,
                author=author
            )
            
            for _ in range(random.randint(0, 5)):
                voter = random.choice(User.objects.all())
                toggle_vote(tip, voter, random.choice(['upvote', 'downvote']))

            self.stdout.write(self.style.SUCCESS(f'Successfully created tip: "{content}" by {author.username}'))

        self.stdout.write(self.style.SUCCESS('Database population completed successfully.'))
        self.stdout.write(self.style.SUCCESS(f'\nSuperuser credentials:\nUsername: {admin_username}\nPassword: {admin_password}'))
        self.stdout.write(self.style.SUCCESS(f'Regular users password: {password}'))

