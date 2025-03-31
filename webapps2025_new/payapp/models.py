from django.db import models
from register.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name="senders", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="recipients", on_delete=models.CASCADE)
    amount = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        return str(self.datetime)