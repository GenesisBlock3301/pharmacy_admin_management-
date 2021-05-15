from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('user-register/', views.register, name='user-register'),
    path('user-login/', views.Login, name='user-login'),
    path('logout/', views.logout_view, name='user-logout')
]
