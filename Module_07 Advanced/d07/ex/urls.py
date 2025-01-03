from django.urls import path
from .views import Login, Logout, Register, ArticlesView, Detail, Publish, Publications, Favourite

urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('articles/<slug:pk>/', Detail.as_view(), name='articles_detail'),
    path('publish/', Publish.as_view(), name='publish'),
    path('publications/', Publications.as_view(), name='publications'),
    path('favourite/', Favourite.as_view(), name='favourite')
]
