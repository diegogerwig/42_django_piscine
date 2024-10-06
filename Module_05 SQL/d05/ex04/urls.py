from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init, name='ex04_init'),
    path('populate/', views.populate, name='ex04_populate'),
    path('display/', views.display, name='ex04_display'),
    path('remove/', views.remove, name='ex04_remove'),
]

