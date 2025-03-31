from django import forms

from register.models import CustomUser

class SendMoney(forms.Form):
    recipient = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    amount = forms.FloatField(label="Amount:", required=True)