from ex.forms.login import LoginForm
from typing import Any
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.views.generic import FormView
from django.urls import reverse_lazy


class Login(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # AuthenticationForm necesita el request
        return kwargs

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You already logged in!')
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: LoginForm):
        user = form.get_user()  # AuthenticationForm proporciona get_user()
        login(self.request, user)
        messages.info(self.request, f"You are now logged in as {user.username}.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)