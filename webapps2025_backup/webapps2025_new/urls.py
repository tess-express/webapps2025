"""
URL configuration for webapps2025_new project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import register.views as register_views
import payapp.views as payapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', payapp_views.home, name='home'),
    path('register/', register_views.register_user, name='register'),
    path('login/', register_views.login_user, name='login'),
    path('home/', payapp_views.home, name='home')
]
