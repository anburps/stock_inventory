from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()
from .forms import *
from .models import *

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = User.objects.create_user(name=name, email=email, phone_number=phone, password=password)
        print("user", user)
        if user:
            return redirect('login')
        else:
            return redirect('register')
        
    return render(request, 'account/register.html')


def login_view(request):
    if request.method == 'POST':
        email_or_phone = request.POST.get('emailPhone')
        password = request.POST.get('password')

        user = None
        if not email_or_phone or not password:
            return redirect('login')

        if '@' in email_or_phone:
            user = User.objects.filter(email=email_or_phone).first()
        else:
            user = User.objects.filter(phone_number=email_or_phone).first()

        if user and check_password(password, user.password):
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')

    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


