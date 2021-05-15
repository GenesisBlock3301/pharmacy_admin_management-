from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
import datetime
import calendar
from django.views import View
from .models import Employee, Customer, SalesManagement, MedicineHistory, CustomerHistory
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


class Dashboard(LoginRequiredMixin, View):
    # @method_decorator(login_required, name='user-login')
    login_url = '/user-login/'
    redirect_field_name = 'user-login'

    def get(self, request):
        my_date = datetime.date.today()
        search = request.GET.get('q')
        # print("search", search.split("-"))
        year, week, day_of_week = my_date.isocalendar()
        first_day, last_day = find_start_ending_day_of_week(year, week)
        if search:
            year, week = str(search).split("-")
            print("Split year week", year, week)
            first_day, last_day = find_start_ending_day_of_week(int(year), int(week[-2:]))
        labels = []
        data = []
        dic = dict()
        print("My date", my_date)
        for single_date in (first_day + datetime.timedelta(n) for n in range(7)):
            date = " ".join(str(single_date).split("-")[::-1])
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            sales = SalesManagement.objects.filter(updated_at=single_date)
            dic[calendar.day_name[day]] = get_selling_sum(sales)
            # labels.append(calendar.day_name[day])
        print(dic)
        for i in dic:
            labels.append(i)
            data.append(dic[i])

        # print(labels)

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


class EmployeeList(View):
    def get(self, request):
        employee = Employee.objects.all()
        # use django model Q for searching
        search = request.GET.get('q')
        # if search anything this time only work this block
        if search:
            employee = Employee.objects.filter(
                Q(employee_name__icontains=search)
            ).distinct()
        # total_selling = get_selling_sum(medicine)
        # total_expense = get_expense_sum(medicine)
        page = request.GET.get('page', 1)

        # call django built in pagination class
        paginator = Paginator(employee, per_page=2)
        try:
            employees = paginator.page(page)
        except PageNotAnInteger as e:
            employees = paginator.page(1)
        except EmptyPage:
            employees = Paginator.page(paginator.num_pages)
        return render(request, 'employee/employee_list.html', {
            'employees': employees,
            # 'total_selling': total_selling,
            # 'total_expense': total_expense,
        })
        # return render(request, 'employee/employee_list.html')


class UpdateEmployee(View):
    def get(self, request, pk):
        employee = get_object_or_404(Employee, id=pk)
        return render(request, 'employee/update-employee.html', {'employee': employee})

    def post(self, request, pk):
        # get or error handle
        employee = get_object_or_404(Employee, pk=pk)
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phonenumber')
        salary = request.POST.get('salary')
        payment = request.POST.get('payment')
        employee.employee_name = name
        employee.address = address
        employee.phone_number = phone_number
        employee.salary_amount = float(salary)
        employee.payment = payment
        employee.save()
        messages.success(request, "Successfully updated")
        return redirect("employee-list")


def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    messages.success(request, 'Successfully deleted')
    return redirect("employee-list")


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
                medicine_price=float(medicine_price),
                payment=float(payment)
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
        paginator = Paginator(customers, per_page=1)
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
            # return redirect('customers-histories')

        messages.success(request, "Successfully updated")
        return redirect("customer-list")


def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    messages.success(request, 'Successfully deleted')
    return redirect("customer-list")


def delete_customer_history(request, pk):
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


class CreateSalesManagement(View):
    def get(self, request):
        return render(request, 'medicine/CreateSalesManagement.html')

    def post(self, request):
        # try:
        medicine_name = request.POST.get('Mname', None)
        location = request.POST.get('location', None)
        description = request.POST.get('description', None)
        original_price = request.POST.get('Oprice', None)
        selling_price = request.POST.get('Sprice', None)
        number_of_medicine = request.POST.get('Nmedicine', None)
        # sell_at_a_time = request.POST.get('Smedicine', None)
        medicine = SalesManagement.objects.create(
            medicine_name=medicine_name,
            location=location,
            description=description,
            original_price=float(original_price),
            selling_price=float(selling_price),
            number_of_medicine=int(number_of_medicine),
        )
        medicine.save()
        messages.success(request, "Created medicine successfully.")
        return redirect('medicine-list')


class SalesManagementList(View):
    def get(self, request):
        sales = SalesManagement.objects.all()
        # use django model Q for searching
        search = request.GET.get('q')
        # if search anything this time only work this block
        if search:
            sales = SalesManagement.objects.filter(
                Q(medicine_name__icontains=search) | Q(created_at__exact=search)
            ).distinct()
        total_selling = get_selling_sum(sales)
        total_expense = get_expense_sum(sales)
        page = request.GET.get('page', 1)
        # call django built in pagination class
        paginator = Paginator(sales, per_page=5)
        try:
            all_sales = paginator.page(page)
        except PageNotAnInteger as e:
            all_sales = paginator.page(1)
        except EmptyPage:
            all_sales = Paginator.page(paginator.num_pages)
        print(">>>>>>>>>>>>>>>>>>", all_sales)
        return render(request, 'medicine/sales_list.html', {
            'medicines': all_sales,
            'total_selling': total_selling,
            'total_expense': total_expense,
        })


class UpdateMedicine(View):
    def get(self, request, pk):
        sale = get_object_or_404(SalesManagement, id=pk)
        return render(request, 'medicine/updateSaleManagement.html', {'sale': sale})

    def post(self, request, pk):
        # get or error handle
        medicine = get_object_or_404(SalesManagement, pk=pk)
        location = request.POST.get('location')
        original_price = request.POST.get('Oprice')
        selling_price = request.POST.get('Sprice')
        sold_at_a_time = request.POST.get('smedicine')
        number_of_medicine = request.POST.get('Nmedicine')
        print(int(sold_at_a_time))
        medicine.location = location
        medicine.original_price = float(original_price)
        medicine.selling_price = float(selling_price)
        medicine.sold_at_a_time = int(sold_at_a_time)
        medicine.number_of_medicine = int(number_of_medicine)
        medicine.save()
        if medicine.number_of_medicine <= 0:
            history = MedicineHistory.objects.create(
                medicine_name=medicine,
                quantity=medicine.sold_number_of_medicine,
                expense=medicine.sold_number_of_medicine * medicine.original_price,
                selling=medicine.sold_medicine_value()
            )
            history.save()
            medicine.sold_number_of_medicine = 0
            medicine.save()
            return redirect('medicine-histories')
        messages.success(request, "Successfully updated")
        return redirect("medicine-list")


# delete medicine from salesmanagement model
def delete_medicine(request, pk):
    medicine = get_object_or_404(SalesManagement, pk=pk)
    medicine.delete()
    messages.success(request, 'Successfully deleted')
    return redirect("medicine-list")


class MedicineHistoryView(View):
    def get(self, request):
        history = MedicineHistory.objects.all()
        # use django model Q for searching
        search = request.GET.get('q')
        # if search anything this time only work this block
        if search:
            history = MedicineHistory.objects.filter(
                Q(medicine_name__medicine_name__icontains=search) | Q(created_at__icontains=search)
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
        return render(request, 'medicine/medicine_history.html', {
            'histories': all_history,
            # 'total_selling': total_selling,
            # 'total_expense': total_expense,
        })


def delete_medicine_history(request, pk):
    history = get_object_or_404(MedicineHistory, pk=pk)
    history.delete()
    messages.success(request, 'Successfully Deleted.')
    return redirect('medicine-histories')


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
