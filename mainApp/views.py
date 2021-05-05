from django.shortcuts import render, redirect
import datetime
import calendar
from django.views import View
from .models import Employee, Customer, SalesManagement
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def register(request):
    return render(request, 'accounts/register.html')


def login(request):
    return render(request, 'accounts/login.html')


class Dashboard(View):
    def get(self, request):
        my_date = datetime.date.today()
        year, week, day_of_week = my_date.isocalendar()
        first_day, last_day = find_start_ending_day_of_week(year, week - 1)
        labels = []
        for single_date in (first_day + datetime.timedelta(n) for n in range(7)):
            single_date = " ".join(str(single_date).split("-")[::-1])
            day = datetime.datetime.strptime(single_date, '%d %m %Y').weekday()
            labels.append(calendar.day_name[day])

        # labels = [
        #     'Sunday',
        #     'Monday',
        #     'Tuesday',
        #     'Wednesday',
        #     'Thursday',
        #     'Friday',
        #     'Saturday'
        # ]
        data = [
            15339,
            20000,
            18483,
            24003,
            23489,
            24092,
            12034
        ]

        return render(request, 'dashboard/index.html', {
            'labels': labels,
            'data': data,
        })


class CreateEmployee(View):
    def get(self, request):
        return render(request, 'employee/create_employee.html')

    def post(self, request):

        try:
            name = request.POST.get('name', None)
            address = request.POST.get('address', None)
            phone_number = request.POST.get('phonenumber', None)
            salary = request.POST.get('salary', None)
            payment = request.POST.get('payment', None)
            print(name, address, phone_number, salary, payment)
            employee = Employee.objects.create(
                employee_name=name,
                address=address,
                phone_number=phone_number,
                salary_amount=salary,
                payment=payment
            )
            employee.save()
            messages.success(request, "Employee Created Successfully")
        except TypeError as e:
            messages.error(request, 'Something is wrong')
        return redirect('create-employee')


class CreateCustomer(View):
    def get(self, request):
        return render(request, 'customer/create_customer.html')

    def post(self, request):

        try:
            name = request.POST.get('name', None)
            address = request.POST.get('address', None)
            phone_number = request.POST.get('phonenumber', None)
            medicine_price = request.POST.get('medicine_price', None)
            payment = request.POST.get('payment', None)
            print(name, address, phone_number, medicine_price, payment)
            customer = Customer.objects.create(
                customer_name=name,
                address=address,
                phone_number=phone_number,
                medicine_price=medicine_price,
                payment=payment
            )
            customer.save()
            messages.success(request, "Customer Created Successfully")
        except TypeError as e:
            messages.error(request, 'Something is wrong')
        return redirect('create-customer')


class CreateSalesManagement(View):
    def get(self, request):
        return render(request, 'sales/CreateSalesManagement.html')

    def post(self, request):
        # try:
        medicine_name = request.POST.get('Mname', None)
        location = request.POST.get('location', None)
        original_price = request.POST.get('Oprice', None)
        selling_price = request.POST.get('Sprice', None)
        number_of_medicine = request.POST.get('Nmedicine', None)
        # sell_at_a_time = request.POST.get('Smedicine', None)
        medicine = SalesManagement.objects.create(
            medicine_name=medicine_name,
            location=location,
            original_price=float(original_price),
            selling_price=float(selling_price),
            number_of_medicine=int(number_of_medicine),
        )
        medicine.save()
        messages.success(request, "Created medicine successfully.")
        return redirect('sales-list')
    # except TypeError as e:
    #     messages.error(request, "Medicine information not created!")


class SalesManagementList(View):
    def get(self, request):
        sales = SalesManagement.objects.all()
        total_selling = get_selling_sum(sales)
        total_expense = get_expense_sum(sales)
        page = request.GET.get('page', 1)
        paginator = Paginator(sales, per_page=3)
        try:
            all_sales = paginator.page(page)
        except PageNotAnInteger as e:
            all_sales = paginator.page(1)
        except EmptyPage as e:
            all_sales = Paginator.page(paginator.num_pages)
        return render(request, 'sales/sales_detail.html', {
            'sales': all_sales,
            'total_selling': total_selling,
            'total_expense': total_expense
        })


# helper function
def find_start_ending_day_of_week(year, week):
    print("Year and Week", year, week)
    first_day_of_week = datetime.datetime.strptime(f"{year}-W{int(week)}-1", '%Y-W%W-%w').date()
    last_day_of_week = first_day_of_week + datetime.timedelta(days=6.9)
    return first_day_of_week, last_day_of_week


def get_selling_sum(sales):
    sum = 0
    for sale in sales:
        sum += sale.sold_medicine_value()
    return sum


def get_expense_sum(sales):
    sum = 0
    for sale in sales:
        sum += sale.expense()
    return sum
