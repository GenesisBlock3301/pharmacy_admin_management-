from django import template
from mainApp.models.customer import Customer

register = template.Library()


def id_filter(value):
    customer = Customer.objects.get(customer_name=value)
    return customer.id


register.filter('id_filter', id_filter)
