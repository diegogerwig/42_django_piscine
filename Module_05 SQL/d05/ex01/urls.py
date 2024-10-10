from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init, name='ex01_init'),
]
