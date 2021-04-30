from django.contrib import admin
from .models import *


class SalesManagementAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'number_of_medicine','original_price','selling_price','created_at')


admin.site.register(SalesManagement, SalesManagementAdmin)
