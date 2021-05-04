from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-employee/', views.CreateEmployee.as_view(), name='create-employee'),
]
