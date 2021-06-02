from django.urls import path
from mainApp.views import employee_views, customer_view, medicine_view, stockless_view

urlpatterns = [
    path('', medicine_view.Dashboard.as_view(), name='dashboard'),

    path('create-employee/', employee_views.CreateEmployee.as_view(), name='create-employee'),
    path('employee-list/', employee_views.EmployeeList.as_view(), name='employee-list'),
    path('update-employee/<int:pk>/', employee_views.UpdateEmployee.as_view(), name='update-employee'),
    path('delete-employee/<int:pk>/', employee_views.delete_employee, name='delete-employee'),
    path('employee-profile/<int:pk>/', employee_views.employee_profile, name='employee-profile'),

    path('create-customer/', customer_view.CreateCustomer.as_view(), name='create-customer'),
    path('customer-list/', customer_view.CustomerList.as_view(), name='customer-list'),
    path('update-customer/<int:pk>/', customer_view.UpdateCustomer.as_view(), name='update-customer'),
    path('delete-customer/<int:pk>/', customer_view.delete_customer, name='delete-customer'),
    path('customer-histories/', customer_view.CustomerHistoryView.as_view(), name='customer-histories'),
    path('customer-histories-delete/<int:pk>/', customer_view.delete_customer_history,
         name='customer-histories-delete'),
    path('customer-profile/<int:pk>/', customer_view.customer_profile, name='customer-profile'),

    path('create-medicine/', medicine_view.CreateSalesManagement.as_view(), name='create-medicine'),
    path('medicine-list/', medicine_view.SalesManagementList.as_view(), name='medicine-list'),
    path('update-medicine/<int:pk>/', medicine_view.UpdateMedicine.as_view(), name='update-medicine'),
    path('delete-medicine/<int:pk>/', medicine_view.delete_medicine, name='delete-medicine'),
    path('medicine-histories/', medicine_view.MedicineHistoryView.as_view(), name='medicine-histories'),
    path('medicine-delete-history/<pk>/', medicine_view.delete_medicine_history, name='medicine-delete-history'),
    path('medicine_detail/<int:pk>/', medicine_view.medicine_detail, name="medicine-detail"),

    path('create-stock-less/', stockless_view.CreateStockLessView.as_view(), name="create-stock-less"),
    path('stock-less-list/', stockless_view.StockLessList.as_view(), name="stock-less-list"),
    path('served/<pk>/', stockless_view.stockless_served, name="served")
]
