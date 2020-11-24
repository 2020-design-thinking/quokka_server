from datetime import datetime
from math import cos, asin, sqrt, pi

from django.db import models

# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
from core.charge import calculate_charge
from core.points import calculate_safety_points
from judge.models import SafetyScore


def distance(lat1, lon1, lat2, lon2):
    p = pi / 180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))


class Drive(models.Model):
    driver = models.ForeignKey('users.User', on_delete=models.CASCADE)
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE)

    start_timestamp = models.DateTimeField(auto_now_add=True)
    end_timestamp = models.DateTimeField(auto_now_add=True)
    ended = models.BooleanField(default=False)

    driving_charge = models.IntegerField(default=0)
    safety_rate = models.FloatField(default=-1)

    dist = models.DecimalField(max_digits=5, decimal_places=1, default=-1)

    discounted_charge = models.IntegerField(default=0)
    charge = models.IntegerField(default=0)

    def calculate_total_distance(self):
        locations = LocationSample.objects.filter(drive=self)
        f_dist = 0
        for i in range(1, len(locations)):
            f_dist += distance(float(locations[i - 1].lat), float(locations[i - 1].lng), float(locations[i].lat),
                               float(locations[i].lng))

        self.dist = f_dist
        self.save()

    def calculate_safety_rate(self):
        if self.safety_rate >= 0:
            return self.safety_rate

        scores = SafetyScore.objects.filter(drive=self)

        average = 0
        for score in scores:
            average += score.score

        if len(scores) == 0:
            average = 0
        else:
            average /= len(scores)

        self.safety_rate = round(average, 1) * 5
        self.save()

    def finish(self):
        self.end_timestamp = datetime.now()
        self.end = True

        self.calculate_total_distance()
        self.calculate_safety_rate()

        self.driving_charge = calculate_charge(self.dist)
        self.discounted_charge = calculate_safety_points(self.safety_rate, self.dist)
        self.charge = max(self.driving_charge - self.discounted_charge, 0)

        self.save()


class LocationSample(models.Model):
    drive = models.ForeignKey('Drive', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    speed = models.IntegerField(default=0)
