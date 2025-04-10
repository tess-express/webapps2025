from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from register.models import User

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            forename = form.cleaned_data.get('forename')
            surname = form.cleaned_data.get('surname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            currency = form.cleaned_data.get('currency')
            u = User(forename=forename, surname=surname, email=email, password=password, currency=currency)
            u.save()
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
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'User logged in')
                return redirect('home')
            else:
                return render(request, 'register/login.html', {'login_user': form, 'error': 'Invalid credentials'})
        else:
            messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'register/login.html', {'login_user': form})