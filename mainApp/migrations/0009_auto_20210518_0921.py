# Generated by Django 3.1.7 on 2021-05-18 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0008_auto_20210518_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='customer_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='stocklessmedicine',
            name='customer',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
