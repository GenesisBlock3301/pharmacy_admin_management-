from django.db import models
from mainApp.models.common import Common, TimeStamp


class Customer(Common, TimeStamp):
    customer_name = models.CharField(max_length=255)
    medicine_price = models.FloatField(default=0.0)
    payment = models.FloatField(blank=True, default=0.0, null=True)
    payment_at_a_time = models.FloatField(default=0)

    def __str__(self):
        return self.customer_name

    class Meta:
        ordering = ('-created_at',)

    def customer_due(self):
        if self.medicine_price > self.payment:
            return self.medicine_price - self.payment
        else:
            return 0

    def save(self, *args, **kwargs):
        if self.payment_at_a_time <= self.medicine_price:
            self.payment += self.payment_at_a_time
            self.payment_at_a_time = 0
        else:
            self.payment = 0
            self.payment_at_a_time = 0
        return super().save(*args, **kwargs)


class CustomerHistory(TimeStamp):
    name = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.FloatField(default=0.0)

    def __str__(self):
        return self.name.customer_name

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = "Customers Histories"
