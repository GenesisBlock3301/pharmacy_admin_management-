from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views import View
from mainApp.models.employee import Employee
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


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
        return redirect('employee-list')


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
