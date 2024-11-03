from django.db.models.query import QuerySet
from django.forms.forms import BaseForm
from django.db import DatabaseError
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from ex.models.article import Article, UserFavouriteArticle
from ex.forms.favourite import FavouriteForm

class Favourite(LoginRequiredMixin, ListView):
    template_name = "favourite.html"
    model = UserFavouriteArticle

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).select_related('article')

    def post(self, request, *args, **kwargs):
        article_id = request.POST.get('article')
        if not article_id:
            messages.error(request, "Invalid article selected.")
            return redirect('favourite')
            
        try:
            favourite = UserFavouriteArticle.objects.get(
                article_id=article_id,
                user=request.user
            )
            favourite.delete()
            messages.success(request, "Successfully removed from favourites.")
        except UserFavouriteArticle.DoesNotExist:
            try:
                article = Article.objects.get(id=article_id)
                UserFavouriteArticle.objects.create(
                    user=request.user,
                    article=article
                )
                messages.success(request, "Successfully added to favourites.")
            except Article.DoesNotExist:
                messages.error(request, "Article not found.")
            except DatabaseError:
                messages.error(request, "Database error occurred.")
                
        return redirect('favourite')