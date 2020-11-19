import random

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.parsers import MultiPartParser

from devices.models import Device
from devices.serializers import DeviceSerializer
from drive.models import Drive


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    parser_classes = (MultiPartParser,)
    queryset = Device.objects.all()

    def get_list(self, request):
        return HttpResponse(serializers.serialize('json', Device.objects.all()))

    def create(self, request):
        if not request.user.is_superuser:
            return HttpResponse(status=403)

        print(request.user)
        name = "쿼카 #{}".format(random.randrange(1, 10000))
        while len(Device.objects.filter(name=name)) > 0:
            name = "쿼카 #{}".format(random.randrange(1, 10000))
        device = Device(name=name)
        device.save()
        return HttpResponse(status=200)

    def delete(self, request, pk):
        if not request.user.is_superuser:
            return HttpResponse(status=403)

        device = get_object_or_404(Device, pk=pk)
        device.delete()
        return HttpResponse(status=200)

    def update(self, request, pk):
        device = get_object_or_404(Device, pk=pk)
        serialize = DeviceSerializer(device, data=request.data)

        if not serialize.is_valid():
            return HttpResponse(400)

        battery = serialize.validated_data.get('battery', None)
        if battery:
            device.battery = battery

        lat = serialize.validated_data.get('lat', None)
        if lat:
            device.lat = lat

        lng = serialize.validated_data.get('lng', None)
        if lng:
            device.lng = lng

        device.save()

        return HttpResponse(status=200)

    def drive(self, request, pk):
        if request.user.is_anonymous:
            return HttpResponse(status=403)

        device = get_object_or_404(Device, pk=pk)

        if device.using:
            return HttpResponse(status=403)

        drv = Drive(user=request.user, device=device)
        drv.save()

        device.using = True
        device.save()

        request.user.last_drive = drv
        request.user.save()

        return JsonResponse({'pk': drv.pk})
