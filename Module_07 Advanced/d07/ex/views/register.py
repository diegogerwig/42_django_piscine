from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from typing import Any
from ex.forms import RegisterForm
from ex.models import UserFavouriteArticle

class Register(CreateView):
    model = UserFavouriteArticle
    form_class = RegisterForm
    template_name = "register.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You are already logged in!')
            return redirect('articles')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful. Welcome aboard!")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(
            self.request, "Unsuccessful registration. Please check the form fields and try again."
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('articles')