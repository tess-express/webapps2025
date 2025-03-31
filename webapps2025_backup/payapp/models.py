from django.db import models
import webapps2025_new.settings as settings
import datetime

class Transaction(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        return str(self.datetime)