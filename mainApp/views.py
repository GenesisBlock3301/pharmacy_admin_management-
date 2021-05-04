from django.shortcuts import render
import datetime
import calendar
from django.views import View


def register(request):
    return render(request, 'accounts/register.html')


def login(request):
    return render(request, 'accounts/login.html')


def dashboard(request):
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


# helper function
def find_start_ending_day_of_week(year, week):
    print("Year and Week", year, week)
    first_day_of_week = datetime.datetime.strptime(f"{year}-W{int(week)}-1", '%Y-W%W-%w').date()
    last_day_of_week = first_day_of_week + datetime.timedelta(days=6.9)
    return first_day_of_week, last_day_of_week
