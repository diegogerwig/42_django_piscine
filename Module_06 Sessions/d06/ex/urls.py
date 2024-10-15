from django.urls import path
from . import views

urlpatterns = [
    path('display/', views.display, name='ex09_display'),
]

