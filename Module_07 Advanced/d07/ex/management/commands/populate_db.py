from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ex.models import Article, UserFavouriteArticle
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cleaning database...')
        UserFavouriteArticle.objects.all().delete()
        Article.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write('Creating users...')
        users = []
        user_data = [
            {'username': 'writer1', 'password': 'urduliz42'},
            {'username': 'writer2', 'password': 'urduliz42'},
            {'username': 'writer3', 'password': 'urduliz42'}
        ]

        for data in user_data:
            user = User.objects.create_user(
                username=data['username'],
                password=data['password']
            )
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')

        titles = [
            "The Future of Technology",
            "Understanding Machine Learning",
            "Web Development Best Practices",
            "Cloud Computing Essentials",
            "Mobile App Development Trends",
            "Database Design Patterns",
            "DevOps and Automation",
            "Cybersecurity Fundamentals",
            "Software Architecture Principles",
            "API Design Guidelines",
            "Python Programming Tips",
            "JavaScript Modern Features",
            "Docker Container Basics",
            "Git Version Control",
            "Data Science Fundamentals"
        ]

        lorem_paragraphs = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
            "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.",
            "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.",
            "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium.",
            "Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus.",
            "Omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet.",
            "Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.",
            "Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur?",
            "Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur?",
            "Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.",
            "Quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.",
            "Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain.",
            "On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized.",
            "These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammeled.",
            "One who avoids pain that produces no resultant pleasure?",
            "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque.",
            "In a free hour, when our power of choice is untrammeled and when nothing prevents our being able to do what we like best."
        ]

        created_articles = []
        articles_by_user = {user.id: 0 for user in users}
        min_articles_per_user = 3
        min_total_articles = 10

        self.stdout.write('Creating articles...')
        while True:
            total_articles = len(created_articles)
            min_user_articles = min(articles_by_user.values())
            
            if total_articles >= min_total_articles and min_user_articles >= min_articles_per_user:
                break
            
            if not titles:  
                titles.append(f"Article {total_articles + 1}")

            potential_authors = [
                user for user in users 
                if articles_by_user[user.id] < min_articles_per_user
            ] if min_user_articles < min_articles_per_user else users
            
            author = random.choice(potential_authors)

            article = Article.objects.create(
                title=titles.pop(0),
                author=author,
                synopsis=random.choice(lorem_paragraphs),
                content="\n\n".join(random.sample(lorem_paragraphs, k=3))
            )
            articles_by_user[author.id] += 1
            created_articles.append(article)
            self.stdout.write(f'Created article: {article.title} by {article.author.username}')

        selected_user = random.choice(users)
        self.stdout.write(f'Creating favourites for user: {selected_user.username}')

        other_articles = [
            article for article in created_articles 
            if article.author != selected_user
        ]

        if len(other_articles) >= 2:
            favourite_articles = random.sample(other_articles, 2)
            for article in favourite_articles:
                UserFavouriteArticle.objects.create(
                    user=selected_user,
                    article=article
                )
                self.stdout.write(f'Added favourite: {article.title} for user {selected_user.username}')

        self.stdout.write(self.style.SUCCESS(f'''
Successfully populated database:
- Created {len(users)} users
- Created {len(created_articles)} articles in total
- Articles per user:
  {"\n  ".join(f"* {user.username}: {articles_by_user[user.id]} articles" for user in users)}
- User {selected_user.username} has 2 favourite articles
'''))