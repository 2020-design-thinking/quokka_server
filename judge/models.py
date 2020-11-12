import os

from django.db import models


def get_upload_path(instance, filename):
    return os.path.join('images', str(instance.drive.pk), filename)


class DrivingImage(models.Model):
    drive = models.ForeignKey('drive.Drive', on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)

    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    speed = models.IntegerField(default=0)

    image = models.ImageField(upload_to=get_upload_path, null=False)

    processed = models.BooleanField(default=False)
    score = models.FloatField(default=0)


class SafetyScore(models.Model):
    drive = models.ForeignKey('drive.Drive', on_delete=models.CASCADE)

    judge_timestamp = models.DateTimeField(auto_now_add=True)

    score = models.FloatField(default=0)

    reason = models.CharField(max_length=100, null=True)
