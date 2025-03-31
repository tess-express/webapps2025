from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from register.models import CustomUser

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
            CustomUser.objects.create_user(email, password, currency, forename=forename, surname=surname)
            return redirect("login")
        messages.error(request, 'Registration failed')
    form = RegisterForm()
    return render(request, 'register/register.html', {'register_user': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'User logged in')
                return render(request, 'payapp/home.html', {'user': user})
            else:
                return render(request, 'register/login.html', {'login_user': form, 'error': 'Invalid credentials'})
        else:
            messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
        return render(request, 'register/login.html', {'login_user': form})