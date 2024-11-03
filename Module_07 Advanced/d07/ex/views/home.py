from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['show_login_form'] = True
            context['login_form'] = AuthenticationForm()
        return context