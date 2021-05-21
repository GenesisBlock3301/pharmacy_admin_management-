from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views import View
from mainApp.models.customer import Customer, CustomerHistory
from mainApp.models.medicine import MedicineHistory
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


class CreateCustomer(View):
    def get(self, request):
        return render(request, 'customer/create_customer.html')

    def post(self, request):

        try:
            name = request.POST.get('name', None)
            address = request.POST.get('address', None)
            phone_number = request.POST.get('phonenumber', None)
            medicine_price = request.POST.get('medicine_price', None)
            if medicine_price == '':
                medicine_price = 0
            # payment = request.POST.get('payment', None)
            # print(name, address, phone_number, medicine_price, payment)
            customer = Customer.objects.create(
                customer_name=name,
                address=address,
                phone_number=phone_number,
                medicine_price=float(medicine_price),
                # payment=float(payment)
            )
            customer.save()
            messages.success(request, "Customer Created Successfully")
        except TypeError as e:
            messages.error(request, 'Something is wrong')
        return redirect('customer-list')


class CustomerList(View):
    def get(self, request):
        customers = Customer.objects.all()
        # use django model Q for searching
        search = request.GET.get('q')
        # if search anything this time only work this block
        if search:
            customers = Customer.objects.filter(
                Q(customer_name__icontains=search)
            ).distinct()
        # total_selling = get_selling_sum(medicine)
        # total_expense = get_expense_sum(medicine)
        page = request.GET.get('page', 1)

        # call django built in pagination class
        paginator = Paginator(customers, per_page=10)
        try:
            customers = paginator.page(page)
        except PageNotAnInteger as e:
            customers = paginator.page(1)
        except EmptyPage:
            customers = Paginator.page(paginator.num_pages)
        return render(request, 'customer/customer_list.html', {
            'customers': customers,
            # 'total_selling': total_selling,
            # 'total_expense': total_expense,
        })
        # return render(request, 'employee/employee_list.html')


class UpdateCustomer(View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, id=pk)
        return render(request, 'customer/update_customer.html', {'customer': customer})

    def post(self, request, pk):
        # get or error handle
        customer = get_object_or_404(Customer, pk=pk)
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phonenumber')
        medicine_price = float(request.POST.get('mprice'))
        # payment = request.POST.get('payment')
        payment_at_a_time = float(request.POST.get('apayment'))

        customer.customer_name = name
        customer.address = address
        customer.phone_number = phone_number
        customer.medicine_price = medicine_price
        customer.payment_at_a_time = payment_at_a_time
        customer.save()
        if customer.medicine_price == customer.payment:
            history = CustomerHistory.objects.create(
                name=customer,
                payment=customer.payment,
            )
            history.save()
            customer.medicine_price = 0
            customer.payment = 0
            customer.save()
            messages.success(request, "Successfully updated")
            return redirect('customer-histories')

        # messages.success(request, "Successfully updated")
        return redirect("customer-list")


def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    messages.success(request, 'Successfully deleted')
    return redirect("customer-list")


class CustomerHistoryView(View):
    def get(self, request):
        history = CustomerHistory.objects.all()
        # use django model Q for searching
        search = request.GET.get('q')
        # if search anything this time only work this block
        if search:
            history = MedicineHistory.objects.filter(
                Q(created_at__icontains=search) | Q(name__customer_name__iscontains=search)
            ).distinct()
        # total_selling = get_selling_sum(sales)
        # total_expense = get_expense_sum(sales)
        page = request.GET.get('page', 1)
        # call django built in pagination class
        paginator = Paginator(history, per_page=5)
        try:
            all_history = paginator.page(page)
        except PageNotAnInteger as e:
            all_history = paginator.page(1)
        except EmptyPage:
            all_history = Paginator.page(paginator.num_pages)
        print("Alll histories", all_history)
        return render(request, 'customer/customer_history.html', {
            'histories': all_history,
            # 'total_selling': total_selling,
            # 'total_expense': total_expense,
        })


def delete_customer_history(request, pk):
    customer = get_object_or_404(CustomerHistory, pk=pk)
    customer.delete()
    messages.success(request, 'Successfully deleted')
    return redirect("customer-list")

def customer_profile(request,pk):
    customer = Customer.objects.get(id=pk)
    return render(request,'customer/customer_profile.html',{'customer':customer})