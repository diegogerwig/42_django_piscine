from django.views.generic import DetailView
from django.contrib import messages
from django.shortcuts import redirect
from django.db import DatabaseError
from ex.models import Article, UserFavouriteArticle

class Detail(DetailView):
    model = Article
    template_name = 'detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_favourite'] = UserFavouriteArticle.objects.filter(
                article=self.object,
                user=self.request.user
            ).exists()
        if hasattr(self.request, 'login_form'):
            context['login_form'] = self.request.login_form
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to manage favorites.")
            return redirect('login')

        self.object = self.get_object()
            
        try:
            favourite = UserFavouriteArticle.objects.get(
                article=self.object,
                user=request.user
            )
            favourite.delete()
            messages.success(request, "Successfully removed from favourites.")
        except UserFavouriteArticle.DoesNotExist:
            try:
                UserFavouriteArticle.objects.create(
                    user=request.user,
                    article=self.object
                )
                messages.success(request, "Successfully added to favourites.")
            except DatabaseError:
                messages.error(request, "Database error occurred.")
                
        return redirect('articles_detail', pk=self.object.pk)