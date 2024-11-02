# from typing import Any, Dict
# from django.http import Http404
# from django.views.generic import DetailView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from ex.forms import FavouriteForm
# from ex.models.article import Article

# class Detail(DetailView):
#     template_name = "detail.html"
#     model = Article
#     context_object_name = 'article'  

#     def get_object(self, queryset=None):
#         try:
#             return Article.objects.select_related('author').get(pk=self.kwargs['pk'])
#         except Article.DoesNotExist:
#             raise Http404("Article does not exist")

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         article = context['article']  
#         context['favouriteForm'] = FavouriteForm(initial={'article': article.id})
#         return context



from typing import Any, Dict
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ex.forms import FavouriteForm
from ex.models.article import Article

class Detail(DetailView):
    template_name = "detail.html"
    model = Article
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.select_related('author')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        article = context['article']
        context.update({
            'favouriteForm': FavouriteForm(article=article),
            'is_favourite': hasattr(article, 'is_favourite') and article.is_favourite(self.request.user) if self.request.user.is_authenticated else False,
        })
        return context