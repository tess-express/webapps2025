from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from register.models import CustomUser

currency_choices = (("gbp", "GBP"), ("eur", "EUR"),  ("usd", "USD"))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    forename = forms.CharField(required=True)
    surname = forms.CharField(required=True)
    currency = forms.ChoiceField(required=True, choices=currency_choices)


    class Meta:
        model = CustomUser
        fields = ("forename", "surname", "email", "password1", "password2", "currency")

class ChangeUserForm(UserChangeForm):
    email = forms.EmailField(required=True)
    forename = forms.CharField(required=True)
    surname = forms.CharField(required=True)
    currency = forms.ChoiceField(required=True, choices=currency_choices)

    class Meta:
        model = CustomUser
        fields = ("forename", "surname", "email", "currency")

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("email", "password")