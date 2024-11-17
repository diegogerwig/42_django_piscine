from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from ex.models import Article
from ex.forms import LoginForm

class Publications(LoginRequiredMixin, ListView):
    template_name = "publications.html"
    model = Article
    context_object_name = 'articles'
    login_url = '/login/'
    redirect_field_name = 'next'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user).order_by('-created')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context