from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from register.managers import CustomUserManager


currency_choices = (("gbp", "GBP"), ("eur", "EUR"),  ("usd", "USD"))




class User(AbstractBaseUser):
    forename = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    currency = models.CharField(max_length=3, choices=currency_choices)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['forename', 'surname']
    objects = CustomUserManager()

    class Meta:
        app_label = 'payapp'

    def __str__(self):
        return self.email