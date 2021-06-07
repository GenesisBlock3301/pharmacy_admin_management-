from django.db import models
from mainApp.models.common import Common, TimeStamp
from mainApp.models.customer import Customer


class Medicine(TimeStamp):
    medicine_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255,null=True,blank=True,default='')
    description = models.TextField(blank=True, null=True, default='')
    location = models.CharField(max_length=50, null=True, blank=True)
    number_of_medicine = models.IntegerField(default=0, null=True, blank=True)
    original_price = models.FloatField(blank=True, null=True)
    selling_price = models.FloatField(blank=True, null=True)
    sold_number_of_medicine = models.IntegerField(default=0, blank=True, null=True)
    sold_at_a_time = models.IntegerField(default=0, blank=True, null=True)
    expire_date = models.DateField(blank=True,null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.medicine_name)

    def selling_profit(self):
        return self.sold_number_of_medicine * self.selling_price

    def sold_medicine_value(self):
        return self.sold_number_of_medicine * self.selling_price

    def expense(self):
        return self.original_price * self.number_of_medicine

    def save(self, *args, **kwargs):
        if self.sold_at_a_time <= self.number_of_medicine:
            self.number_of_medicine -= self.sold_at_a_time
            self.sold_number_of_medicine += self.sold_at_a_time
            self.sold_at_a_time = 0
        return super().save(*args, **kwargs)


class MedicineHistory(TimeStamp):
    # one to many relation
    medicine_name = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    expense = models.FloatField(default=0.0)
    selling = models.FloatField(default=0.0)

    def __str__(self):
        return self.medicine_name.medicine_name

    def profit(self):
        return self.selling - self.expense

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Medicine Histories'
