from django.db import models
from django.utils import timezone


class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    medicine_price = models.FloatField()
    payment = models.FloatField(blank=True, default=0.0, null=True)
    payment_at_a_time = models.FloatField(default=0)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.customer_name

    def customer_due(self):
        if self.medicine_price > self.payment:
            return self.medicine_price - self.payment

    def save(self, *args, **kwargs):
        if self.payment_at_a_time <= self.medicine_price:
            self.payment += self.payment_at_a_time
            self.payment_at_a_time = 0
            return super().save(*args, **kwargs)


class CustomerHistory(models.Model):
    name = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.FloatField(default=0.0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name.customer_name

    class Meta:
        ordering = ('created_at',)
        verbose_name_plural = "Customers Histories"


class Employee(models.Model):
    employee_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=16)
    salary_amount = models.FloatField()
    payment = models.CharField(default='', max_length=255)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.employee_name


class SalesManagement(models.Model):
    medicine_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True, default='')
    location = models.CharField(max_length=50, null=True, blank=True)
    number_of_medicine = models.IntegerField(default=0, null=True, blank=True)
    original_price = models.FloatField(blank=True, null=True)
    selling_price = models.FloatField(blank=True, null=True)
    sold_number_of_medicine = models.IntegerField(default=0, blank=True, null=True)
    sold_at_a_time = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.medicine_name)

    # def selling_profit(self):
    #     return self.number_of_medicine * self.selling_price

    def sold_medicine_value(self):
        return self.sold_number_of_medicine * self.selling_price

    def expense(self):
        return self.original_price * self.number_of_medicine

    # def history_expense(self):
    #     return self.

    def save(self, *args, **kwargs):
        if self.sold_at_a_time <= self.number_of_medicine:
            self.number_of_medicine -= self.sold_at_a_time
            self.sold_number_of_medicine += self.sold_at_a_time
            self.sold_at_a_time = 0
        return super().save(*args, **kwargs)


class MedicineHistory(models.Model):
    # one to many relation
    medicine_name = models.ForeignKey(SalesManagement, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    expense = models.FloatField(default=0.0)
    selling = models.FloatField(default=0.0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.medicine_name.medicine_name

    def profit(self):
        return self.selling - self.expense

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Medicine Histories'
