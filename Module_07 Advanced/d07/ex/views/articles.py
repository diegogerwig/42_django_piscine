from typing import Any, Dict
from django.views.generic import ListView
from ex.models import Article
from ex.forms import LoginForm

class ArticlesView(ListView):
    template_name = "articles.html"
    model = Article
    queryset = Article.objects.filter().order_by('-created')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm()  
        return context