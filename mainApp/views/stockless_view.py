from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from mainApp.models.medicine import Medicine
from mainApp.models.customer import Customer
from mainApp.models.stockless import StockLessMedicine
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


class CreateStockLessView(View):
    def get(self, request):
        return render(request, 'stockless_medicine/create_stockless.html')

    def post(self, request):
        print("Working")
        medicine_name = request.POST.get('Mname', None)
        customer_name = request.POST.get('cname', None)
        company_name = request.POST.get('Coname', None)
        description = request.POST.get('description', None)
        original_price = float(request.POST.get('Oprice'))
        selling_price = float(request.POST.get('Sprice'))
        quantity = int(request.POST.get('quantity', None))
        print(medicine_name, customer_name, quantity)
        try:
            medicine = Medicine.objects.get(medicine_name=medicine_name)
            if medicine:
                return redirect('medicine-list')
        except Medicine.DoesNotExist:
            medicine = Medicine.objects.create(
                medicine_name=medicine_name,
                company_name=company_name,
                description=description,
                original_price=original_price,
                selling_price=selling_price,
                number_of_medicine=quantity
            )
            medicine.save()
        try:
            customer = Customer.objects.get(customer_name=customer_name)
            print("get customer")
        except Customer.DoesNotExist:
            customer = Customer.objects.create(customer_name=customer_name)
            print("Customer work")
            # customer.save()
        stock_less = StockLessMedicine.objects.create(
            medicine=medicine,
            customer=customer,
            quantity=quantity,
            # is_served=True if is_served == 'on' else False
        )
        stock_less.save()
        customer_new_due = stock_less.quantity * stock_less.medicine.selling_price
        print(customer_new_due, stock_less.customer.customer_due())
        customer.medicine_price = customer_new_due + stock_less.customer.customer_due()
        customer.save()

        return redirect('customer-list')
