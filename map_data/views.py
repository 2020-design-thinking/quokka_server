import random

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.parsers import MultiPartParser, FormParser

from devices.models import Device
from devices.serializers import DeviceSerializer
from drive.models import Drive
from map_data.models import SafeZone, Station
from map_data.serializers import SafeZoneSerializer, StationSerializer


class MapDataViewSet(viewsets.ModelViewSet):
    serializers = {
        'get_safe_zone_list': SafeZoneSerializer,
        'get_station_list': StationSerializer,
        'default': None
    }
    parser_classes = (FormParser,)
    queryset = SafeZone.objects.all()

    def get_safe_zone_list(self, request):
        res = []
        for safe_zone in SafeZone.objects.all():
            res.append({
                'pk': safe_zone.pk,
                'lat': safe_zone.lat,
                'lng': safe_zone.lng,
                'radius': safe_zone.radius
            })
        return JsonResponse(res, safe=False)

    def get_station_list(self, request):
        res = []
        for station in Station.objects.all():
            res.append({
                'pk': station.pk,
                'lat': station.lat,
                'lng': station.lng
            })
        return JsonResponse(res, safe=False)

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])