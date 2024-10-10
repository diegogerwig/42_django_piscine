from django.urls import path
from . import views

urlpatterns = [
    path('populate/', views.populate, name='ex03_populate'),
    path('display/', views.display, name='ex03_display'),
]
