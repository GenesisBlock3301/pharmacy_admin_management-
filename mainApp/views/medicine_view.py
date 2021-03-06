from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
import datetime
import calendar
from django.views import View
from mainApp.models.medicine import Medicine, MedicineHistory
from mainApp.models.customer import Customer
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
        year, week, day_of_week = my_date.isocalendar()
        first_day, last_day = find_start_ending_day_of_week(year, week - 1)
        if search:
            year, week = str(search).split("-")
            # print("Split year week", year, week)
            first_day, last_day = find_start_ending_day_of_week(int(year), int(week[-2:]))
        labels = []
        data = []
        dic = dict()
        # print("My date", my_date)
        for single_date in (first_day + datetime.timedelta(n) for n in range(7)):
            date = " ".join(str(single_date).split("-")[::-1])
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            medicine = Medicine.objects.filter(updated_at=single_date)
            dic[calendar.day_name[day]] = get_selling_sum(medicine)
            # labels.append(calendar.day_name[day])
        # print(dic)
        for i in dic:
            labels.append(i)
            # data.append(dic[i])
        data = [1000, 3000, 500, 7700, 6000, 3500, 898]
        # print(labels)

        return render(request, 'dashboard/index.html', {
            'labels': labels,
            'data': data,
        })


class CreateSalesManagement(View):
    def get(self, request):
        return render(request, 'medicine/CreateSalesManagement.html')

    def post(self, request):
        # try:
        medicine_name = request.POST.get('Mname', None)
        company_name = request.POST.get('coname', None)
        location = request.POST.get('location', None)
        category = request.POST.get('cat', None)
        description = request.POST.get('description', None)
        original_price = request.POST.get('Oprice', None)
        selling_price = request.POST.get('Sprice', None)
        number_of_medicine = request.POST.get('Nmedicine', None)
        expire_date = str(request.POST.get('edate', None))
        edate = " ".join(str(expire_date).split("/")[::-1])
        # sell_at_a_time = request.POST.get('Smedicine', None)
        try:
            medicine = Medicine.objects.create(
                medicine_name=medicine_name,
                location=location,
                category=category,
                company_name=company_name,
                description=description,
                original_price=float(original_price),
                selling_price=float(selling_price),
                number_of_medicine=int(number_of_medicine),
                expire_date=edate
            )
            medicine.save()
            messages.success(request, "Created medicine successfully.")
        except:
            messages.error(request, "Medicine already exists")
        return redirect('medicine-list')


class SalesManagementList(View):
    def get(self, request):
        medicines = Medicine.objects.all()
        # use django model Q for searching
        search = request.GET.get('q')
        # if search anything this time only work this block
        if search:
            medicines = Medicine.objects.filter(
                Q(medicine_name__icontains=search) | Q(category__icontains=search)
            ).distinct()
        total_selling = get_selling_sum(medicines)
        total_expense = get_expense_sum(medicines)
        page = request.GET.get('page', 1)
        # call django built in pagination class
        paginator = Paginator(medicines, per_page=4)
        try:
            all_medicine = paginator.page(page)
        except PageNotAnInteger as e:
            all_medicine = paginator.page(1)
        except EmptyPage:
            all_medicine = Paginator.page(paginator.num_pages)
        # print(">>>>>>>>>>>>>>>>>>", all_sales)
        return render(request, 'medicine/sales_list.html', {
            'medicines': all_medicine,
            'total_selling': total_selling,
            'total_expense': total_expense,
        })


class UpdateMedicine(View):
    def get(self, request, pk):
        medicine = get_object_or_404(Medicine, id=pk)
        # customer = Customer.objects.get(customer_name=medicine.)
        return render(request, 'medicine/updateSaleManagement.html', {'medicine': medicine})

    def post(self, request, pk):
        # get or error handle
        medicine = get_object_or_404(Medicine, pk=pk)
        customer_name = request.POST.get('cname', None)
        # company_name = request.POST.get('coname', None)
        # description = request.POST.get('description', None)
        address = request.POST.get('address')
        phone_number = request.POST.get('phonenumber')
        try:
            customer = Customer.objects.get(customer_name=customer_name)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(
                customer_name=customer_name,
                address=address,
                phone_number=phone_number
            )
        location = request.POST.get('location')
        # category = request.POST.get('location')
        original_price = request.POST.get('Oprice')
        selling_price = request.POST.get('Sprice')
        sold_at_a_time = request.POST.get('smedicine')
        number_of_medicine = request.POST.get('Nmedicine')
        # print(int(sold_at_a_time))

        medicine.location = location
        medicine.original_price = float(original_price)
        medicine.selling_price = float(selling_price)
        medicine.sold_at_a_time = int(sold_at_a_time)
        medicine.number_of_medicine = int(number_of_medicine)
        medicine.save()
        new_due = int(sold_at_a_time) * float(selling_price)
        customer.medicine_price += new_due
        # customer.payment += int(sold_at_a_time) * float(selling_price)
        customer.save()
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
            messages.success(request, "Successfully updated")
            return redirect('medicine-histories')
        return redirect("medicine-list")


# delete medicine from salesManagement model
def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
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
        # print("Alll histories", all_history)
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


def medicine_detail(request, pk):
    medicine = Medicine.objects.get(id=pk)
    return render(request, 'medicine/medicine_detail.html', {'medicine': medicine})


# helper function

def find_start_ending_day_of_week(year, week):
    # print("Year and Week", year, week)
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
