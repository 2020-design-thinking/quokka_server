from datetime import datetime

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser

from devices.models import Device
from devices.serializers import DeviceSerializer
from drive.models import Drive, LocationSample
from drive.serializers import LocationSampleSerializer, DriveSerializer
from judge.models import DrivingImage
from judge.serializers import DrivingImageSerializer
from core.charge import calculate_charge
from core.points import calculate_points, calculate_charge_points, calculate_safety_points


class DriveViewSet(viewsets.ModelViewSet):
    serializers = {
        'update': LocationSampleSerializer,
        'image': DrivingImageSerializer,
        'default': None
    }
    parser_classes = (FormParser,)
    queryset = Drive.objects.all()

    def update(self, request, pk):
        serialize = LocationSampleSerializer(data=request.data)

        if not serialize.is_valid():
            return HttpResponse(status=400)

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

    def finish(self, request, pk):
        drive = get_object_or_404(Drive, pk=pk)

        if drive.driver != request.user:
            return HttpResponse(status=403)

        drive.finish()

        device = drive.device
        device.using = False
        device.save()

        drive.driver.add_points(calculate_points(drive.dist), "DRIVE", drive)
        drive.driver.add_points(calculate_safety_points(drive.safety_rate, drive.dist), "SAFETY", drive)
        drive.driver.add_points(calculate_charge_points(device), "CHARGE", drive)

        # TODO: 거리, 요금, 안전 평점, 추가된 포인트 정보 제공
        return JsonResponse(DriveSerializer(drive).data, safe=False)

    def status(self, request, pk):
        drive = get_object_or_404(Drive, pk=pk)

        if drive.driver != request.user:
            return HttpResponse(status=403)

        drive.calculate_total_distance()

        last_warn = drive.get_last_warning()

        print("--drive status--")
        print(0 if last_warn is None else last_warn.judge_timestamp.timestamp())
        print(-1 if last_warn is None else last_warn.reason)

        return JsonResponse({
            'dist': drive.dist,
            'charge': calculate_charge(drive.dist),
            'last_warn_timestamp': 0 if last_warn is None else int(last_warn.judge_timestamp.timestamp()),
            'last_warn_type': -1 if last_warn is None else last_warn.reason
        })

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])
