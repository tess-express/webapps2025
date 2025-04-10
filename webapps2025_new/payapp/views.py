from django.db import transaction, OperationalError
from django.shortcuts import render, redirect
from payapp.forms import SendMoney, RequestMoney, RespondToRequest
from django.contrib import messages
from currency_converter import CurrencyConverter
from django.contrib.auth import get_user_model
from register.models import Balance
from payapp.models import Transaction, Request
import decimal
from django.db.models import Q
import requests

User = get_user_model()
c = CurrencyConverter()

#Renders the home page
def home(request):
    if request.user.is_superuser:
        #Includes a list of all users to be displayed on the homepage if the user is an admin
        context = {"users" : list(User.objects.all()), "balances": list(Balance.objects.all())}
    else:
        context = {"users" : []}
    return render(request, "payapp/home.html", context)

def view_transactions(request):
    if request.user.is_superuser:
        # Shows all transactions made if the user is an admin
        transactions = list(Transaction.objects.all())
    else:
        # If the user is not an admin, only transactions with the user as the sender or recipient are shown
        transactions = list(Transaction.objects.filter(Q(sender=request.user) | Q(recipient=request.user)))
    return render(request, "payapp/transactions.html", {"transaction_list": transactions})

def view_requests(request):
    if request.user.is_superuser:
        #Shows all requests if the user is an admin
        requests = list(Request.objects.all())
    else:
        # If the user is not an admin, only requests with the user as the requester or recipient are shown
        requests = list(Request.objects.filter(Q(requester=request.user) | Q(recipient=request.user)))
    return render(request, "payapp/requests.html", {"request_list": requests})

def respond_requests(request):
    if request.method == 'POST':
        form = RespondToRequest(request.POST)
        if form.is_valid():
            #Foreign key to link to a Request object
            t_request = form.cleaned_data['request']
            #Either "accept" or "deny"
            response = form.cleaned_data['response']
            #User objects
            requester = t_request.requester
            recipient = t_request.recipient
            #Amount of money requested (in requester's currency)
            amount_requested = t_request.amount
            #Attributes of the Request object - the requester and recipient's currencies
            req_currency = t_request.requester_currency
            rec_currency = t_request.recipient_currency
            #Amount of money requested (converted into recipient's currency)
            amount_to_send = decimal.Decimal(c.convert(amount_requested, req_currency, rec_currency))
            #Balance objects related to the requesters and recipients
            req_balance = requester.balance
            rec_balance = recipient.balance
            #Changes the status of the request from "pending" to either "accepted" or "denied"
            Request.objects.filter(requester=requester, recipient=recipient, amount=amount_to_send).update(
                status=response)
            if response == 'accepted':
                #Checks if the recipient has enough money to accept the request
                if amount_to_send <= rec_balance.balance:
                    #Transaction object is created
                    t = Transaction(sender=recipient, recipient=requester, amount=amount_to_send, sender_currency=rec_currency, recipient_currency=req_currency)
                    t.save()
                    try:
                        with transaction.atomic():
                            #Moves the money from the recipient's account to the requester's (converted into the respective currencies)
                            rec_balance.balance -= amount_to_send
                            rec_balance.save()
                            req_balance.balance += amount_requested
                            req_balance.save()
                            messages.success(request, "Transaction completed")
                    except OperationalError:
                        messages.info(request, f"Transfer operation is not possible now.")
                    return redirect("home")
                else:
                    Request.objects.filter(requester=requester, recipient=recipient, amount=amount_to_send).update(
                        status="pending")
                    messages.error(request, "Insufficient funds")
                    return redirect("requests")
            else:
                messages.success(request, "Request denied")
                return redirect("home")
    form = RespondToRequest()
    return render(request, 'payapp/requestrespond.html', {'request_respond': form})

def request_money(request):
    if request.method == "POST":
        form = RequestMoney(request.POST)
        if form.is_valid():
            requester = request.user
            recipient = form.cleaned_data.get('recipient')
            amount_requested = form.cleaned_data.get('amount')
            req_b = requester.balance
            rec_b = recipient.balance
            req_curr = req_b.currency.upper()
            rec_curr = rec_b.currency.upper()
            amount_to_send = decimal.Decimal(c.convert(amount_requested, req_curr, rec_curr))
            if requester != recipient and rec_b.balance > amount_to_send > 0:
                r = Request(requester=requester, recipient=recipient, amount=amount_to_send, requester_currency=req_curr, recipient_currency=rec_curr)
                r.save()
                messages.success(request, "Request sent successfully")
                return home(request)
            elif amount_to_send > req_b.balance:
                messages.error(request, "Insufficient balance")
            elif amount_requested < 0:
                messages.error(request, "You can't send negative money")
            elif requester == recipient:
                messages.error(request, "You can't send money to yourself")
    form = RequestMoney()
    return render(request, 'payapp/requestmoney.html', {'request_money': form})

def send_money(request):
    if request.method == "POST":
        form = SendMoney(request.POST)
        if form.is_valid():
            sender = request.user
            recipient = form.cleaned_data.get('recipient')
            s_balance = sender.balance
            r_balance = recipient.balance
            sent_amount = form.cleaned_data.get('amount')
            sender_currency = s_balance.currency.upper()
            recipient_currency = r_balance.currency.upper()
            received_amount = decimal.Decimal(c.convert(sent_amount, sender_currency, recipient_currency))

            if sender != recipient and s_balance.balance > sent_amount > 0:
                t = Transaction(sender=sender, recipient=recipient, amount=sent_amount, sender_currency=sender_currency, recipient_currency=recipient_currency)
                t.save()
                try:
                    with transaction.atomic():
                        s_balance.balance -= sent_amount
                        s_balance.save()
                        r_balance.balance += received_amount
                        r_balance.save()
                except OperationalError:
                    messages.info(request, f"Transfer operation is not possible now.")

                home(request)
            elif sender == recipient:
                messages.error(request, "You can't send money to yourself")
            elif sent_amount < 0:
                messages.error(request, "You can't send negative money")
            elif sent_amount > s_balance.balance:
                messages.error(request, "Insufficient balance")
        messages.error(request, 'Money was not sent.')
    form = SendMoney()
    return render(request, 'payapp/sendmoney.html', {'send_money': form})


