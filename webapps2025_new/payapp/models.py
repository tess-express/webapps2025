from django.db import models

import register.models
from register.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()
currency_choices = (("gbp", "GBP"), ("eur", "EUR"), ("usd", "USD"))
request_statuses = (("accepted", "accepted"), ("rejected", "rejected"), ("pending", "pending"))

class Transaction(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, primary_key=True)
    sender = models.ForeignKey(register.models.CustomUser, related_name="senders", on_delete=models.CASCADE)
    recipient = models.ForeignKey(register.models.CustomUser, related_name="recipients", on_delete=models.CASCADE)
    sender_currency = models.CharField(max_length=3, choices=currency_choices, default="GBP")
    recipient_currency = models.CharField(max_length=3, choices=currency_choices, default="GBP")
    amount = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        details = ''
        details += f'Sender        : {self.sender}\n'
        details += f'Recipient     : {self.recipient}\n'
        details += f'Date+Time     : {self.datetime}\n'
        return details


class Request(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    requester = models.ForeignKey(CustomUser, related_name="req_requesters", on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name="req_recipients", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    requester_currency = models.CharField(max_length=3, choices=currency_choices, default="GBP")
    recipient_currency = models.CharField(max_length=3, choices=currency_choices, default="GBP")
    status = models.CharField(max_length=8, choices=request_statuses, default="pending")

    class Meta:
        ordering = ["datetime"]

    def __str__(self):
        details = ''
        details += f'Requester      : {self.requester}\n'
        details += f'Recipient      : {self.recipient}\n'
        details += f'Date+Time      : {self.datetime}\n'
        return details

