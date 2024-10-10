from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init, name='ex08_init'),
    path('populate/', views.populate, name='ex08_populate'),
    path('display/', views.display, name='ex08_display'),
]

