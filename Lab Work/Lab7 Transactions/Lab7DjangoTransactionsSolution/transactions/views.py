from django.db import transaction, OperationalError
from django.db.models import F
from django.shortcuts import render
from . import models
from transactions.forms import PointsTransferForm
from .models import Points
from django.contrib import messages


# Create your views here.
def points_transfer(request):
    if request.method == 'POST':
        form = PointsTransferForm(request.POST)

        if form.is_valid():

            src_username = form.cleaned_data["enter_your_username"]
            dst_username = form.cleaned_data["enter_destination_username"]
            points_to_transfer = form.cleaned_data["enter_points_to_transfer"]

            src_points = models.Points.objects.select_related().get(name__username=src_username)
            dst_points = models.Points.objects.select_related().get(name__username=dst_username)

            try:
                with transaction.atomic():
                    src_points.points = src_points.points - points_to_transfer
                    src_points.save()

                    dst_points.points = dst_points.points + points_to_transfer
                    dst_points.save()
            except OperationalError:
                messages.info(request, f"Transfer operation is not possible now.")

            # Points.objects.filter(name__username=src_username).update(points=F('points')-points_to_transfer)
            # Points.objects.filter(name__username=dst_username).update(points=F('points')+points_to_transfer)

        return render(request, "transactions/points.html", {"src_points": src_points, "dst_points": dst_points})

    else:
        form = PointsTransferForm()

    return render(request, "transactions/pointstransfer.html", {"form": form})
