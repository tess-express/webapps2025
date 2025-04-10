from django.apps import AppConfig
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_migrate

def createadmin(sender, **kwargs):
    from register.models import CustomUser, Balance
    email = "admin@gmail.com"
    forename = "Tess"
    surname = "Jones"
    password = "admin"
    currency = "GBP"
    b = Balance(currency=currency)
    b.save()
    CustomUser.objects.create_superuser(email=email, password=password, forename=forename, surname=surname,
                                            balance=b)

#Creates a single admin account on database startup
class PayappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payapp'

    def ready(self):
        post_migrate.connect(createadmin, sender=self)

