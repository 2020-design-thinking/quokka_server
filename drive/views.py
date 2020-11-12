from datetime import datetime

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view

from devices.models import Device
from devices.serializers import DeviceSerializer
from drive.models import Drive, LocationSample
from drive.serializers import LocationSampleSerializer


@api_view(['POST'])
def update(request, pk):
    if request.method == 'POST':
        serialize = LocationSampleSerializer(data=request.data)

        lat = serialize.validated_data.get('lat', None)
        lng = serialize.validated_data.get('lng', None)
        speed = serialize.validated_data.get('speed', None)

        if None in (lat, lng, speed):
            return HttpResponse(status=400)

        drive = get_object_or_404(Drive, pk=pk)

        if drive.user != request.user:
            return HttpResponse(status=403)

        sample = LocationSample(drive=drive, lat=lat, lng=lng, speed=speed)
        sample.save()

        device = drive.device
        device.lat = lat
        device.lng = lng
        device.save()

        return HttpResponse(status=200)

    return HttpResponse(status=400)


@api_view(['POST'])
def end(request, pk):
    if request.method == 'POST':
        drive = get_object_or_404(Drive, pk=pk)

        if drive.user != request.user:
            return HttpResponse(status=403)

        drive.end_timestamp = datetime.now()
        drive.end = True
        drive.save()

        device = drive.device
        device.using = False
        device.save()

        # TODO: Calculate a charge, safety_rate
