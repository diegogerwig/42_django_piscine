from django.urls import path
from . import views

urlpatterns = [
    path('populate/', views.populate, name='ex07_populate'),
    path('display/', views.display, name='ex07_display'),
    path('remove/', views.remove, name='ex07_remove'),
    path('update/', views.update, name='ex07_update'),
]

