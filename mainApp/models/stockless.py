from django.db import models
from mainApp.models.common import TimeStamp
from mainApp.models.customer import Customer
from mainApp.models.common import Common


class StockLessMedicine(TimeStamp,Common):
    # medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='medicines')
    customer = models.CharField(max_length=255, blank=True, null=True)
    medicine_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True, default='')
    original_price = models.FloatField(blank=True, null=True)
    selling_price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    is_served = models.BooleanField(default=False)

    def __str__(self):
        return self.medicine_name
