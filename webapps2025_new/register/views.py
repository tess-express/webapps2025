from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm, RegisterAdminForm
from django.contrib import messages
from register.models import CustomUser, Balance
from currency_converter import CurrencyConverter
from decimal import Decimal
from payapp.views import home

c = CurrencyConverter()
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            forename = form.cleaned_data.get('forename')
            surname = form.cleaned_data.get('surname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            currency = form.cleaned_data.get('currency')
            currency = currency.upper()
            b = Decimal(c.convert(100, "GBP", currency))
            balance = Balance(balance=b, currency=currency)
            balance.save()
            u = CustomUser.objects.create_user(email=email, password=password, forename=forename, surname=surname, balance=balance)
            u.save()
            return redirect("login")
        messages.error(request, 'Registration failed')
    form = RegisterForm()
    return render(request, 'register/register.html', {'register_user': form})

def register_admin(request):
    if request.method == 'POST':
        form = RegisterAdminForm(request.POST)
        if form.is_valid():
            forename = form.cleaned_data.get('forename')
            surname = form.cleaned_data.get('surname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            currency = form.cleaned_data.get('currency')
            currency = currency.upper()
            b = Decimal(c.convert(100, "GBP", currency))
            balance = Balance(balance=b, currency=currency)
            balance.save()
            u = CustomUser.objects.create_superuser(email=email, password=password, forename=forename, surname=surname, balance=balance)
            u.save()
            return redirect("login")
        messages.error(request, 'Registration failed')
    form = RegisterAdminForm()
    return render(request, 'register/adminregister.html', {'register_admin': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                balance = user.balance
                login(request, user)
                messages.success(request, 'User logged in')
                currency_symbol = "£"
                match balance.currency:
                    case 'USD':
                        currency_symbol = '$'
                    case 'EUR':
                        currency_symbol = '€'
                context = {'user': user, "currency_symbol": currency_symbol}
                return render(request, 'payapp/home.html', context)
            else:
                return render(request, 'register/login.html', {'login_user': form, 'error': 'Invalid credentials'})
        else:
            messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
        return render(request, 'register/login.html', {'login_user': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'User logged out')
    return redirect('home')