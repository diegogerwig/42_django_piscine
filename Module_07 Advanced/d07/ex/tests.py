from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, UserFavoriteArticle
from django.contrib.messages import get_messages

class ArticleAccessTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        # Create a test article
        self.article = Article.objects.create(
            title='Test Article',
            author=self.user,
            synopsis='Test Synopsis',
            content='Test Content'
        )

    def test_protected_views_redirect_anonymous_users(self):
        """
        Test that anonymous users are redirected to login when accessing protected views
        """
        protected_urls = [
            reverse('favourite'),
            reverse('publications'),
            reverse('publish'),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login/', response.url)

    def test_protected_views_accessible_to_logged_users(self):
        """
        Test that logged-in users can access protected views
        """
        self.client.login(username='testuser', password='testpass123')
        
        protected_urls = [
            reverse('favourite'),
            reverse('publications'),
            reverse('publish'),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_register_view_inaccessible_to_logged_users(self):
        """
        Test that logged-in users cannot access the registration page
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('articles'))

    def test_prevent_duplicate_favorites(self):
        """
        Test that users cannot add the same article to favorites twice
        """
        self.client.login(username='testuser2', password='testpass123')
        
        # First attempt should succeed
        response = self.client.post(reverse('favourite'), {
            'article_id': self.article.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            UserFavoriteArticle.objects.filter(
                user=self.user2,
                article=self.article
            ).exists()
        )
        
        # Second attempt should fail
        response = self.client.post(reverse('favourite'), {
            'article_id': self.article.id
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify only one favorite entry exists
        favorite_count = UserFavoriteArticle.objects.filter(
            user=self.user2,
            article=self.article
        ).count()
        self.assertEqual(favorite_count, 1)

    def test_favorite_view_template_protected(self):
        """
        Test that the favorite template is only accessible to logged-in users
        """
        response = self.client.get(reverse('favourite'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_publications_template_protected(self):
        """
        Test that the publications template is only accessible to logged-in users
        """
        response = self.client.get(reverse('publications'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_publish_template_protected(self):
        """
        Test that the publish template is only accessible to logged-in users
        """
        response = self.client.get(reverse('publish'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_error_message_on_duplicate_favorite(self):
        """
        Test that appropriate error message is shown when trying to add duplicate favorite
        """
        self.client.login(username='testuser2', password='testpass123')
        
        # Add article to favorites first time
        self.client.post(reverse('favourite'), {'article_id': self.article.id})
        
        # Try to add same article again
        response = self.client.post(reverse('favourite'), {
            'article_id': self.article.id
        }, follow=True)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.tags == 'error' for message in messages))
