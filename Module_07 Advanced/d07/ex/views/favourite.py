from typing import Any, Dict
from django.db import DatabaseError
from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from ex.models import Article, UserFavouriteArticle
from ex.forms import LoginForm

class Favourite(LoginRequiredMixin, ListView):
    template_name = "favourite.html"
    model = UserFavouriteArticle
    context_object_name = 'favourites'
    login_url = '/login/'
    redirect_field_name = 'next'

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user
        ).select_related('article').order_by('-article__created')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context

    def post(self, request, *args: Any, **kwargs: Any):
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