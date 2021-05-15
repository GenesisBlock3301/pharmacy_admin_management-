from django.contrib.auth import login as user_login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        password1 = request.POST.get('password1', None)
        if password == password1:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            user = authenticate(username=username, email=email, password=password)
            user_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Wrong operation')
    return render(request, 'accounts/register.html')


def Login(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            user_login(request,user)
            return redirect('dashboard')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('user-login')
