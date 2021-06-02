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
        return render(request, 'stockless/create_stockless.html')

    def post(self, request):
        print("Working")
        medicine_name = request.POST.get('Mname', None)
        customer_name = request.POST.get('cname', None)
        address = request.POST.get('address', None)
        phone_number = request.POST.get('phonenumber', None)
        company_name = request.POST.get('Coname', None)
        description = request.POST.get('description', None)
        original_price = float(request.POST.get('Oprice'))
        selling_price = float(request.POST.get('Sprice'))
        quantity = int(request.POST.get('quantity', None))

        try:
            customer = Customer.objects.get(customer_name=customer_name)
            print("get customer")
        except Customer.DoesNotExist:
            customer = Customer.objects.create(customer_name=customer_name, address=address, phone_number=phone_number)
            print("Customer work")
            # customer.save()
        stock_less = StockLessMedicine.objects.create(
            customer=customer.customer_name,
            medicine_name=medicine_name,
            company_name=company_name,
            description=description,
            original_price=original_price,
            selling_price=selling_price,
            quantity=quantity,
            # is_served=True if is_served == 'on' else False
        )
        stock_less.save()
        customer_new_due = stock_less.quantity * stock_less.selling_price
        # print(customer_new_due, customer.customer_due())
        customer.medicine_price = customer_new_due + customer.customer_due()
        customer.save()

        return redirect('stock-less-list')


class StockLessList(View):
    def get(self, request):
        stock_less = StockLessMedicine.objects.all()
        # use django model Q for searching
        search = request.GET.get('q')
        # if search anything this time only work this block
        if search:
            stock_less = StockLessMedicine.objects.filter(
                customer__icontains=search
            ).distinct()
        # total_selling = get_selling_sum(medicine)
        # total_expense = get_expense_sum(medicine)
        page = request.GET.get('page', 1)

        # call django built in pagination class
        paginator = Paginator(stock_less, per_page=10)
        try:
            stock_less = paginator.page(page)
        except PageNotAnInteger as e:
            stock_less = paginator.page(1)
        except EmptyPage:
            stock_less = Paginator.page(paginator.num_pages)
        return render(request, 'stockless/stock_list.html', {
            'stock_less': stock_less,
        })


def stockless_served(request, pk):
    stockless = StockLessMedicine.objects.get(id=pk)
    stockless.is_served = True
    customer = Customer.objects.get(customer_name=stockless.customer)
    customer.payment += stockless.balance()
    customer.save()
    stockless.quantity = 0
    stockless.save()
    print(stockless.balance())
    return redirect('stock-less-list')
