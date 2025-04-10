from django import forms

from register.models import CustomUser
from .models import Request

request_choices = [("accepted", "Accept"), ("denied", "Deny")]

#Form to allow users to send money to one another
class SendMoney(forms.Form):
    recipient = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    amount = forms.DecimalField(decimal_places=2, max_digits=10)

#Form to allow a user to request money from another user
class RequestMoney(forms.Form):
    recipient = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    amount = forms.DecimalField(decimal_places=2, max_digits=10)

#Form to allow a user to respond to a payment request
class RespondToRequest(forms.Form):
    request = forms.ModelChoiceField(queryset=Request.objects)
    response = forms.ChoiceField(choices=request_choices)
