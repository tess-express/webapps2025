from django.urls import path, include
from . import views
from register import views as register_views
from django.contrib import admin

urlpatterns = [
    path('payapp/', include('payapp.urls')),
]