from datetime import datetime

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser

from devices.models import Device
from devices.serializers import DeviceSerializer
from drive.models import Drive, LocationSample
from drive.serializers import LocationSampleSerializer
from judge.models import DrivingImage
from judge.serializers import DrivingImageSerializer
from core.charge import calculate_charge
from core.safety_rate import calculate_safety_rate


class DriveViewSet(viewsets.ModelViewSet):
    serializers = {
        'update': LocationSampleSerializer,
        'image': DrivingImageSerializer,
        'default': None
    }
    parser_classes = (MultiPartParser,)
    queryset = Drive.objects.all()

    def update(self, request, pk):
        serialize = LocationSampleSerializer(data=request.data)

        lat = serialize.validated_data.get('lat', None)
        lng = serialize.validated_data.get('lng', None)
        speed = serialize.validated_data.get('speed', None)

        if None in (lat, lng, speed):
            return HttpResponse(status=400)

        drive = get_object_or_404(Drive, pk=pk)

        if drive.driver != request.user:
            return HttpResponse(status=403)

        sample = LocationSample(drive=drive, lat=lat, lng=lng, speed=speed)
        sample.save()

        device = drive.device
        device.lat = lat
        device.lng = lng
        device.save()

        return HttpResponse(status=200)

    def end(self, request, pk):
        drive = get_object_or_404(Drive, pk=pk)

        if drive.driver != request.user:
            return HttpResponse(status=403)

        drive.end_timestamp = datetime.now()
        drive.end = True
        drive.save()

        device = drive.device
        device.using = False
        device.save()

        charge = calculate_charge(drive)
        safety_rate = calculate_safety_rate(drive)

        drive.charge = charge
        drive.safety_rate = safety_rate
        drive.save()

        return HttpResponse(status=200)

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])
