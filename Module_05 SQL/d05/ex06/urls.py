from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init),
    path('populate/', views.populate, name='ex06_populate'),
    path('display/', views.display, name='ex06_display'),
    path('remove/', views.remove, name='ex06_remove'),
    path('update/', views.update, name='ex06_update'),
]
