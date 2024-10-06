from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init, name='ex02_init'),
    path('populate/', views.populate, name='ex02_populate'),
    path('display/', views.display, name='ex02_display'),
]
