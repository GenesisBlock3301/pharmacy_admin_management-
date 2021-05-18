from django.db import models


class Common(models.Model):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

    class Meta:
        abstract = True


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)
