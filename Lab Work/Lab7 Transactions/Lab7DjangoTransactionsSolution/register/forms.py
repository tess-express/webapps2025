from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from transactions.models import Points


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    points = forms.IntegerField()

    class Meta:
        model = User
        fields = ("username", "points", "email", "password1", "password2")

    def save(self, *args, **kwargs):
        instance = super(RegisterForm, self).save(*args, **kwargs)
        Points.objects.create(name=instance, points=self.cleaned_data['points'])
        return instance
