from django.contrib import admin
from mainApp.models.customer import *
from mainApp.models.employee import *
from mainApp.models.medicine import *
from mainApp.models.stockless import *

class SalesManagementAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'medicine_name', 'number_of_medicine', 'sold_number_of_medicine', 'original_price', 'selling_price',
       )
    readonly_fields = ['sold_number_of_medicine']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'address', 'phone_number', 'medicine_price', 'payment']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_name',
        'address',
        'phone_number',
        'salary_amount',
        'payment',
    )


class MedicineHistoryAdmin(admin.ModelAdmin):
    list_display = ['medicine_name', 'quantity', 'selling']


class CustomerHistoryAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'payment' ]


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Medicine, SalesManagementAdmin)
admin.site.register(MedicineHistory, MedicineHistoryAdmin)
admin.site.register(CustomerHistory, CustomerHistoryAdmin)
admin.site.register(StockLessMedicine)
