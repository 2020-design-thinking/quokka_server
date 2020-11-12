from rest_framework import serializers
from .models import LocationSample


class LocationSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationSample
        fields = ['lat', 'lng', 'speed']
