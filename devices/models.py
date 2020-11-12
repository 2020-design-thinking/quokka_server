from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    battery = models.FloatField(default=0)
    last_user_id = models.IntegerField(default=-1)

    using = models.BooleanField(default=False)
