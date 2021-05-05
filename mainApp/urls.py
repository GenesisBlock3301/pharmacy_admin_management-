from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('create-employee/', views.CreateEmployee.as_view(), name='create-employee'),
    path('create-customer/', views.CreateCustomer.as_view(), name='create-customer'),
    path('create-medicine/', views.CreateSalesManagement.as_view(), name='create-medicine'),
    path('sales-list/', views.SalesManagementList.as_view(), name='sales-list'),
]
