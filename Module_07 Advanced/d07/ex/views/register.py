# from django.http.request import HttpRequest
# from django.http.response import HttpResponse
# from django.shortcuts import redirect
# from django.views.generic import FormView
# from django.contrib.auth import login
# from django.contrib import messages
# from django.urls import reverse_lazy
# from typing import Any
# from ..forms import RegisterForm


# class Register(FormView):
#     template_name = "register.html"
#     form_class = RegisterForm
#     success_url = reverse_lazy('articles')

#     def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
#         if self.request.user.is_authenticated:
#             messages.error(self.request, 'You already logined!')
#             return redirect('articles')
#         return super().get(request, *args, **kwargs)

#     def form_valid(self, form: RegisterForm):
#         user = form.save()
#         login(self.request, user)
#         messages.success(self.request, "Registration successful.")
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         messages.error(
#             self.request, "Unsuccessful registration. Invalid information.")
#         return super().form_invalid(form)


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
    success_url = reverse_lazy('profile')

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You are already logged in!')
            return redirect('profile')
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