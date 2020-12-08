from django.db import models
from django.utils import timezone

from core.reserve import RESERVE_TIME


class Device(models.Model):
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    battery = models.FloatField(default=0)
    last_user_id = models.IntegerField(default=-1)

    using = models.BooleanField(default=False)

    reserve = models.ForeignKey('users.User', null=True, on_delete=models.SET_NULL)
    reserve_time = models.DateTimeField(null=True)

    def is_reserved(self, user):
        if self.reserve_time is None or self.reserve is None:
            return False
        if self.reserve == user:
            return False
        return (timezone.now() - self.reserve_time).total_seconds() <= RESERVE_TIME

    def clear_reserve(self):
        self.reserve = None
        self.reserve_time = None
