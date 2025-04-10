from django import forms
from django.contrib.auth.forms import UserCreationForm
from register.models import User

currency_choices = (("gbp", "GBP"), ("eur", "EUR"),  ("usd", "USD"))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    forename = forms.CharField(required=True)
    surname = forms.CharField(required=True)
    currency = forms.ChoiceField(required=True, choices=currency_choices)

    class Meta:
        model = User
        fields = ("forename", "surname", "email", "password1", "password2", "currency")

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")