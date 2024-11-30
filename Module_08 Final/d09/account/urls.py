from django.urls import path
from account.views.auth_views import account_view, login_view, logout_view, register_view

urlpatterns = [
    path('account/', account_view, name='account'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]
