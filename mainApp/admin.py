from django.contrib import admin
from .models import *


class SalesManagementAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'medicine_name', 'number_of_medicine', 'sold_number_of_medicine', 'original_price', 'selling_price',
        'created_at')
    readonly_fields = ['sold_number_of_medicine']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'address', 'phone_number', 'medicine_price', 'payment', 'created_at']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_name',
        'address',
        'phone_number',
        'salary_amount',
        'payment',
        'created_at'
    )


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(SalesManagement, SalesManagementAdmin)
