from django.db import DatabaseError
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from ex.models import Article
from ex.forms import PublishForm

class Publish(CreateView):
    model = Article
    form_class = PublishForm
    template_name = "publish.html"
    success_url = reverse_lazy('articles')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        try:
            return super().form_valid(form)
        except DatabaseError:
            messages.error(self.request, "Unsuccessful publish. DatabaseError")
            return redirect('articles')

    def form_invalid(self, form):
        messages.error(self.request, "Unsuccessful publish. Invalid information.")
        return super().form_invalid(form)