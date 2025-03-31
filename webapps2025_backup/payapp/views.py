from django.shortcuts import render
from payapp.forms import SendMoney
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "payapp/home.html")

def sendmoney(request):
    if request.method == "POST":
        form = SendMoney(request.POST)
        if form.is_valid():
            sender = request.user
            recipient = form.cleaned_data.get('recipient')
            amount = form.cleaned_data.get('amount')
            currency = recipient.currency
            if sender == recipient:
                messages.error(request, "You cannot send money to yourself")
            elif amount < 0:
                messages.error(request, "Amount cannot be negative")
            