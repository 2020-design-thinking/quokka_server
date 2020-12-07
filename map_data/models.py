from django.db import models

from drive.models import distance


class SafeZone(models.Model):
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    radius = models.FloatField(default=0)

    def test(self, lat, lng):
        return distance(self.lat, self.lng, lat, lng) <= self.radius


class Station(models.Model):
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)


def is_in_safe_zone(lat, lng):
    for safe_zone in SafeZone.objects.all():
        if safe_zone.test(lat, lng):
            return True
    return False
