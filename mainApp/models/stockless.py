from django.db import models
from mainApp.models.common import TimeStamp
from mainApp.models.customer import Customer
from mainApp.models.medicine import Medicine


class StockLessMedicine(TimeStamp):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='medicines')
    customer = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    is_served = models.BooleanField(default=False)

    def __str__(self):
        return self.medicine.medicine_name
