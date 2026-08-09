from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='users.register'),
    path('login', views.user_login, name='users.login'),
    path('logout', views.user_logout, name='users.logout'),
]