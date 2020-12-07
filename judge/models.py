import os

from django.db import models


def get_upload_path(instance, filename):
    return os.path.join('images', str(instance.drive.pk), filename)


class DrivingImage(models.Model):
    drive = models.ForeignKey('drive.Drive', on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)

    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    speed = models.IntegerField(default=0)

    image = models.ImageField(upload_to=get_upload_path, null=False)

    processed = models.BooleanField(default=False)
    score = models.FloatField(default=0)


class SafetyScore(models.Model):
    drive = models.ForeignKey('drive.Drive', on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)

    judge_timestamp = models.DateTimeField(auto_now_add=True)

    score = models.IntegerField(default=0)  # [0, 10]

    reason = models.IntegerField(default=0)
