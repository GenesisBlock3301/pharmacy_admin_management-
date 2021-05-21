from django.db import models
from mainApp.models.common import Common, TimeStamp


class Employee(Common, TimeStamp):
    image = models.ImageField(upload_to='employee/')
    employee_name = models.CharField(max_length=255)
    salary_amount = models.FloatField()
    payment = models.CharField(default='', max_length=255)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.employee_name
