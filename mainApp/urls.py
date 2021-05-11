from django.urls import path
from . import views

urlpatterns = [
    # path('register/', views.register, name="register"),
    # path('login/', views.login, name="login"),
    path('', views.Dashboard.as_view(), name='dashboard'),

    path('create-employee/', views.CreateEmployee.as_view(), name='create-employee'),
    path('employee-list/', views.EmployeeList.as_view(), name='employee-list'),
    path('update-employee/<int:pk>/', views.UpdateEmployee.as_view(), name='update-employee'),
    path('delete-employee/<int:pk>/', views.delete_employee, name='delete-employee'),

    path('create-customer/', views.CreateCustomer.as_view(), name='create-customer'),
    path('customer-list/', views.CustomerList.as_view(), name='customer-list'),
    path('update-customer/<int:pk>/', views.UpdateCustomer.as_view(), name='update-customer'),
    path('delete-customer/<int:pk>/', views.delete_customer, name='delete-customer'),

    path('create-medicine/', views.CreateSalesManagement.as_view(), name='create-medicine'),
    path('medicine-list/', views.SalesManagementList.as_view(), name='medicine-list'),
    path('update-medicine/<int:pk>/', views.UpdateMedicine.as_view(), name='update-medicine'),
    path('delete-medicine/<int:pk>/', views.delete_medicine, name='delete-medicine'),

    path('histories/', views.MedicineHistoryView.as_view(), name='histories'),
    path('delete-history/<pk>/', views.delete_history, name='delete-history')
]
