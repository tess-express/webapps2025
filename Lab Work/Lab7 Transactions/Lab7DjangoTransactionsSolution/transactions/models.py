from django.contrib.auth.models import User
from django.db import models


class Points(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=100)

    def __str__(self):
        details = ''
        details += f'Username     : {self.name}\n'
        details += f'Points       : {self.points}\n'
        return details


class PointsTransfer(models.Model):
    enter_your_username = models.CharField(max_length=50)
    enter_destination_username = models.CharField(max_length=50)
    enter_points_to_transfer = models.IntegerField()

    def __str__(self):
        details = ''
        details += f'Your username            : {self.enter_your_username}\n'
        details += f'Destination username     : {self.enter_destination_username}\n'
        details += f'Points To Transfer         : {self.enter_points_to_transfer}\n'
        return details

