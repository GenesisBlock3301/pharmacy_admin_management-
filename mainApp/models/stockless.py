from django.db import models
from mainApp.models.common import TimeStamp
from mainApp.models.common import Common


class StockLessMedicine(TimeStamp, Common):
    # medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='medicines')
    customer = models.CharField(max_length=255, blank=True, null=True)
    medicine_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True, default='')
    original_price = models.FloatField(blank=True, null=True)
    selling_price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField()
    is_served = models.BooleanField(default=False)

    def __str__(self):
        return str(self.medicine_name)

    def balance(self):
        if (self.quantity is not None and self.selling_price is not None) or (
                self.quantity > 0 and self.selling_price > 0):
            return self.quantity * self.selling_price
        else:
            return 0
