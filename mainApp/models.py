from django.db import models


# Create your models here.
class SalesManagement(models.Model):
    medicine_name = models.CharField(max_length=255, unique=True)
    number_of_medicine = models.IntegerField(default=0)
    original_price = models.FloatField()
    selling_price = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.medicine_name

    def expense(self):
        return self.original_price * self.number_of_medicine

    def profit(self):
        sell_medicine_amount = self.selling_price * self.number_of_medicine
        profit = sell_medicine_amount - self.expense()
        if profit > 0:
            return profit

    def loss(self):
        sell_medicine_amount = self.selling_price * self.number_of_medicine
        loss = sell_medicine_amount - self.expense()
        if loss < 0:
            return loss

    def selling(self):
        return self.selling_price * self.number_of_medicine
