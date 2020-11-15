from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    birth = models.DateField()

    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    email = models.EmailField(_('email address'), blank=False)

    points = models.IntegerField('points', default=0)
    safety_rate = models.FloatField('safety_rate', default=0)

    last_drive = models.ForeignKey('drive.Drive', null=True, on_delete=models.SET_NULL)
