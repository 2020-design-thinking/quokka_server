from rest_framework import serializers
from .models import SafeZone, Station


class SafeZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafeZone
        fields = '__all__'


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'
