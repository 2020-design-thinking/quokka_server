from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone

from devices.models import Device


class User(AbstractUser):
    birth = models.DateField()

    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    email = models.EmailField(_('email address'), blank=False)

    points = models.IntegerField('points', default=0)
    safety_rate = models.FloatField('safety_rate', default=0)

    last_drive = models.ForeignKey('drive.Drive', null=True, on_delete=models.SET_NULL)

    reserve_penalty = models.BooleanField(default=False)

    def add_points(self, amount, reason, drive=None):
        if amount == 0:
            return

        transaction = PointTransaction(user=self, amount=amount, reason=reason, drive=drive)
        transaction.save()

        self.points += amount
        self.save()

    def is_reserved(self):
        return self.get_reserved_device() is not None

    def get_reserved_device(self):
        for device in Device.objects.filter(reserve=self):
            if device.is_reserved():
                return device
        return None

    def reserve(self, device):
        device.reserve = self
        device.reserve_time = timezone.now()
        device.save()

    def cancel_reserve(self):
        if not self.is_reserved():
            return
        device = self.get_reserved_device()
        device.reserve = None
        device.reserve_time = None
        device.save()


class PointTransaction(models.Model):
    user = models.ForeignKey('users.User', null=False, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    reason = models.CharField(max_length=100, blank=False)
    drive = models.ForeignKey('drive.Drive', null=True, on_delete=models.SET_NULL)
