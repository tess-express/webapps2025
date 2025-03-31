from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from register.models import CustomUser
from .forms import UserCreationForm, ChangeUserForm

admin.site.register(CustomUser)