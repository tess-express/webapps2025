from django.urls import path, include
from payapp import views
from register import views as register_views
from django.contrib import admin

urlpatterns = [
    # path('payapp/', include('webapps2025.urls')),
    path('admin/', admin.site.urls),
    path('register/', register_views.register_user, name='register'),
    path('login/', register_views.login_user, name='login')
]