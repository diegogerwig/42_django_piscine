from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.utils.translation import activate
from ex.models import Article, UserFavouriteArticle


class ArticleAccessTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123',
            email='test2@example.com'
        )

    def setUp(self):
        self.client = Client()
        activate('en')  # Activate English language for tests
        self.article = Article.objects.create(
            title='Test Article',
            author=self.user,
            synopsis='Test Synopsis',
            content='Test Content'
        )



    ### favourites views, publications and publish as well as their templates are only accessible by registered users

    def test_1_protected_views_accessible_to_logged_users(self):
        """Test that logged-in users can access protected views"""
        self.assertTrue(
            self.client.login(username='testuser', password='testpass123')
        )
        
        protected_urls = [
            reverse('favourite'),
            reverse('publications'),
            reverse('publish'),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)



    ### A registered user cannot access the new user creation form

    def test_2_register_view_inaccessible_to_logged_users(self):
        """Test that logged-in users cannot access the registration page"""
        self.assertTrue(
            self.client.login(username='testuser', password='testpass123')
        )
        
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('articles'))



    ### A user cannot add the same article twice in their favorite list

    def test_3_prevent_duplicate_favorites(self):
        """Test that users cannot add the same article to favorites twice"""
        self.assertTrue(
            self.client.login(username='testuser2', password='testpass123')
        )
        
        # First attempt should succeed
        response = self.client.post(
            reverse('favourite'),
            {'article': self.article.id},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify the favorite was added
        self.assertTrue(
            UserFavouriteArticle.objects.filter(
                user=self.user2,
                article=self.article
            ).exists()
        )
        
        # Second attempt should not create duplicate
        response = self.client.post(
            reverse('favourite'),
            {'article': self.article.id},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        
        # Should remove the favorite instead
        self.assertFalse(
            UserFavouriteArticle.objects.filter(
                user=self.user2,
                article=self.article
            ).exists()
        )
