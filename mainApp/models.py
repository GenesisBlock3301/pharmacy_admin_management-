from django.db import models


class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    medicine_price = models.FloatField()
    payment = models.FloatField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

    def customer_due(self):
        if self.medicine_price > self.payment:
            return self.medicine_price - self.payment


class Employee(models.Model):
    employee_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=16)
    salary_amount = models.FloatField()
    payment = models.FloatField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.employee_name

    def salary_due(self):
        if self.salary_amount > self.payment:
            return self.salary_amount - self.payment


class SalesManagement(models.Model):
    medicine_name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=50)
    number_of_medicine = models.IntegerField(default=0)
    original_price = models.FloatField()
    selling_price = models.FloatField()
    sold_number_of_medicine = models.IntegerField(default=0, blank=True, null=True)
    sold_at_a_time = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.medicine_name

    # def selling_profit(self):
    #     return self.number_of_medicine * self.selling_price

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
