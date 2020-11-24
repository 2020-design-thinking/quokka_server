from datetime import datetime

from django.db import models


class Device(models.Model):
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    battery = models.FloatField(default=0)
    last_user_id = models.IntegerField(default=-1)

    using = models.BooleanField(default=False)

    reserve = models.ForeignKey('users.User', null=True, on_delete=models.SET_NULL)
    reserve_time = models.DateTimeField(null=True)

    def is_reserved(self):
        return self.reserve is not None
