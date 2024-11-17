from django.contrib.auth.models import User
from django.db import models
from .article import Article

class UserFavouriteArticle(models.Model):
    user = models.ForeignKey(
        User, 
        verbose_name="UserFavouriteArticle user", 
        on_delete=models.CASCADE, 
        null=False
    )
    article = models.ForeignKey(
        Article, 
        verbose_name="UserFavouriteArticle article", 
        on_delete=models.CASCADE, 
        null=False
    )

    def __str__(self) -> str:
        return str(self.article.title)