from django.db import models


class Drive(models.Model):
    driver = models.ForeignKey('users.User', on_delete=models.CASCADE)
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE)

    start_timestamp = models.DateTimeField(auto_now_add=True)
    end_timestamp = models.DateTimeField(auto_now_add=True)
    ended = models.BooleanField(default=False)

    charge = models.IntegerField(default=0)
    safety_rate = models.FloatField(default=0)


class LocationSample(models.Model):
    drive = models.ForeignKey('Drive', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    speed = models.IntegerField(default=0)
