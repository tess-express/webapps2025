from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from currency_converter import CurrencyConverter
from decimal import Decimal
c = CurrencyConverter()

currency_choices = [("gbp", "GBP"), ("eur", "EUR"),  ("usd", "USD")]

#Custom user model with email as the primary key
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email shoudn't be empty")
        if not password:
            raise ValueError("Password shoudn't be empty")
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)


        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

#Model containing a user's balance and currency
class Balance(models.Model):
    id = models.AutoField(primary_key=True)
    balance = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=3, choices=currency_choices, default="GBP")

    def __str__(self):
        details = ''
        details += f'ID             : {self.id}\n'
        details += f'Balance        : {self.balance}\n'
        return details

    class Meta:
        app_label = 'register'
        verbose_name = 'Balance'
        verbose_name_plural = 'Balances'

#User model extending the AbstractBaseUser model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, primary_key=True)
    forename = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    balance = models.OneToOneField(Balance, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        app_label = 'register'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

