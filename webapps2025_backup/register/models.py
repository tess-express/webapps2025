from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from currency_converter import CurrencyConverter
c = CurrencyConverter()

currency_choices = (("gbp", "GBP"), ("eur", "EUR"),  ("usd", "USD"))

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, currency="GBP", **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("Email shoudn't be empty")
        if not password:
            raise ValueError("Password shoudn't be empty")
        balance = c.convert(100, "GBP", currency)
        email = self.normalize_email(email)
        user = CustomUser(email=email, balance=balance, currency=currency, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)


        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    forename = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    currency = models.CharField(max_length=3, choices=currency_choices)
    is_staff = models.BooleanField(default=False)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        app_label = 'register'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email