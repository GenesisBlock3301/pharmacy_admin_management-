# Generated by Django 3.1.7 on 2021-05-18 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_remove_stocklessmedicine_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stocklessmedicine',
            old_name='customer_name',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='stocklessmedicine',
            old_name='medicine_name',
            new_name='medicine',
        ),
    ]