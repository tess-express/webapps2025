from django.contrib import admin
from .models import Transaction, Request

admin.site.register(Transaction)
admin.site.register(Request)