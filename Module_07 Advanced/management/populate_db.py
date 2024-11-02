from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ex.models import Article 
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        # Limpiar la base de datos
        self.stdout.write('Cleaning database...')
        Article.objects.all().delete()
        User.objects.all().delete()

        # Crear usuarios
        self.stdout.write('Creating users...')
        users = []
        user_data = [
            {
                'username': 'writer1',
                'password': 'urduliz42'
            },
            {
                'username': 'writer2',
                'password': 'urduliz42'
            },
            {
                'username': 'writer3',
                'password': 'urduliz42'
            }
        ]

        for data in user_data:
            user = User.objects.create_user(
                username=data['username'],
                password=data['password']
            )
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')

        # Crear artículos
        self.stdout.write('Creating articles...')
        articles_data = [
            {
                'title': 'First Article: Introduction to Programming',
                'author': users[0],
                'synopsis': 'A beginner\'s guide to programming concepts and best practices',
                'content': '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                          Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                          Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
                          nisi ut aliquip ex ea commodo consequat.'''
            },
            {
                'title': 'Web Development Trends 2024',
                'author': users[0],
                'synopsis': 'Exploring the latest trends in web development for 2024',
                'content': '''Duis aute irure dolor in reprehenderit in voluptate velit 
                          esse cillum dolore eu fugiat nulla pariatur. Excepteur sint 
                          occaecat cupidatat non proident, sunt in culpa qui officia 
                          deserunt mollit anim id est laborum.'''
            },
            {
                'title': 'Data Science Fundamentals',
                'author': users[1],
                'synopsis': 'Understanding the basics of data science and analytics',
                'content': '''Sed ut perspiciatis unde omnis iste natus error sit voluptatem 
                          accusantium doloremque laudantium, totam rem aperiam, eaque ipsa 
                          quae ab illo inventore veritatis et quasi architecto beatae 
                          vitae dicta sunt explicabo.'''
            },
            {
                'title': 'Artificial Intelligence in 2024',
                'author': users[2],
                'synopsis': 'How AI is transforming industries and our daily lives',
                'content': '''Nemo enim ipsam voluptatem quia voluptas sit aspernatur 
                          aut odit aut fugit, sed quia consequuntur magni dolores eos 
                          qui ratione voluptatem sequi nesciunt.'''
            },
            {
                'title': 'Cybersecurity Best Practices',
                'author': users[2],
                'synopsis': 'Essential security practices for modern applications',
                'content': '''At vero eos et accusamus et iusto odio dignissimos ducimus 
                          qui blanditiis praesentium voluptatum deleniti atque corrupti 
                          quos dolores et quas molestias excepturi sint occaecati 
                          cupiditate non provident.'''
            }
        ]

        for data in articles_data:
            article = Article.objects.create(
                title=data['title'],
                author=data['author'],
                synopsis=data['synopsis'],
                content=data['content']
            )
            self.stdout.write(f'Created article: {article.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))
