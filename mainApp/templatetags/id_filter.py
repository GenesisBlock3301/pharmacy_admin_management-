from django import template
from mainApp.models.customer import Customer
import datetime

register = template.Library()


def id_filter(value):
    customer = Customer.objects.get(customer_name=value)
    return customer.id


def expire_date(value):
    my_date = datetime.date.today()
    if my_date == value:
        return True


register.filter('id_filter', id_filter)
register.filter('expire_date', expire_date)
