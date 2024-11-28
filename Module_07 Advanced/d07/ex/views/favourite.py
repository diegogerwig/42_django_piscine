# from typing import Any, Dict
# from django.db import DatabaseError
# from django.shortcuts import redirect
# from django.views.generic import ListView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib import messages
# from ex.models import Article, UserFavouriteArticle
# from ex.forms import LoginForm

# class Favourite(LoginRequiredMixin, ListView):
#     template_name = "favourite.html"
#     model = UserFavouriteArticle
#     context_object_name = 'favourites'
#     login_url = '/login/'
#     redirect_field_name = 'next'

#     def get_queryset(self):
#         return self.model.objects.filter(
#             user=self.request.user
#         ).select_related('article').order_by('-article__created')

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context['login_form'] = LoginForm()
#         return context

#     def post(self, request, *args: Any, **kwargs: Any):
#         article_id = request.POST.get('article')
#         if not article_id:
#             messages.error(request, "Invalid article selected.")
#             return redirect('favourite')
            
#         try:
#             favourite = UserFavouriteArticle.objects.get(
#                 article_id=article_id,
#                 user=request.user
#             )
#             favourite.delete()
#             messages.success(request, "Successfully removed from favourites.")
#         except UserFavouriteArticle.DoesNotExist:
#             try:
#                 article = Article.objects.get(id=article_id)
#                 UserFavouriteArticle.objects.create(
#                     user=request.user,
#                     article=article
#                 )
#                 messages.success(request, "Successfully added to favourites.")
#             except Article.DoesNotExist:
#                 messages.error(request, "Article not found.")
#             except DatabaseError:
#                 messages.error(request, "Database error occurred.")
                
#         return redirect('favourite')

from typing import Any, Dict
from django.db import DatabaseError
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from ex.models import Article, UserFavouriteArticle
from ex.forms import LoginForm

class Favourite(CreateView):
    template_name = "favourite.html"
    model = UserFavouriteArticle
    success_url = reverse_lazy('favourite')
    fields = []  # We don't need form fields since we handle the POST manually
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        # Get all favorites for the current user with related article and author data
        context['object_list'] = UserFavouriteArticle.objects.filter(
            user=self.request.user
        ).select_related(
            'article', 
            'article__author'
        ).order_by('-article__created')
        return context
    
    def post(self, request, *args, **kwargs):
        article_id = request.POST.get('article')
        
        if not article_id:
            messages.error(request, "Invalid article selected.")
            return redirect('favourite')
            
        try:
            article = Article.objects.get(id=article_id)
            favorite, created = UserFavouriteArticle.objects.get_or_create(
                user=request.user,
                article=article,
                defaults={'user': request.user, 'article': article}
            )
            
            if not created:  # If it already existed, we remove it
                favorite.delete()
                messages.success(request, "Successfully removed from favourites.")
            else:
                messages.success(request, "Successfully added to favourites.")
                
        except Article.DoesNotExist:
            messages.error(request, "Article not found.")
        except DatabaseError:
            messages.error(request, "Database error occurred.")
        
        # Get the next URL from POST data or default to favourite view
        next_url = request.POST.get('next', 'favourite')
        return redirect(next_url)