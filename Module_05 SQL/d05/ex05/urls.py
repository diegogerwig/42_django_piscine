from django.urls import path
from . import views

urlpatterns = [
    path('populate/', views.populate, name='ex05_populate'),
    path('display/', views.display, name='ex05_display'),
    path('remove/', views.remove, name='ex05_remove'),
]
