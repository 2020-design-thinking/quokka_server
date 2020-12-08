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


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    parser_classes = (FormParser,)
    queryset = Device.objects.all()

    def get_list(self, request):
        res = []
        for device in Device.objects.all():
            res.append({
                'pk': device.pk,
                'lat': device.lat,
                'lng': device.lng,
                'battery': device.battery,
                'using': device.using,
                'reserved': device.is_reserved(request.user)
            })
        return JsonResponse(res, safe=False)

    def create(self, request):
        if not request.user.is_superuser:
            return HttpResponse(status=403)

        device = Device()
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
            return HttpResponse(status=400)

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
            return HttpResponse("INUSE", status=400)

        if device.is_reserved(request.user) and device.reserve.id != request.user.id:
            return HttpResponse("RESERVED", status=400)

        device.clear_reserve()

        drv = Drive(driver=request.user, device=device)
        drv.save()

        device.using = True
        device.save()

        request.user.last_drive = drv
        request.user.save()

        return JsonResponse({'pk': drv.pk})

    def reserve(self, request, pk):
        if request.user.is_anonymous:
            return HttpResponse(status=403)

        if request.user.reserve_penalty:
            return JsonResponse({'message': 'RESERVE_PENALTY'}, status=400)

        if request.user.is_reserved():
            return JsonResponse({'message': 'YOU_ALREADY_RESERVED'}, status=400)

        device = get_object_or_404(Device, pk=pk)

        if device.is_reserved(request.user):
            return JsonResponse({'message': 'DEVICE_RESERVED'}, status=400)

        request.user.reserve(device)

        return JsonResponse({'message': 'SUCCESS'}, status=200)
