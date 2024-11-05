from django.urls import path
from . import views

urlpatterns = [
    path('', views.init, name='ex01_init'),
]
