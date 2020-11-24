from rest_framework import serializers
from .models import LocationSample, Drive


class LocationSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationSample
        fields = ['lat', 'lng', 'speed']


class DriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drive
        fields = '__all__'
