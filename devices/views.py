import random

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view

from devices.models import Device
from devices.serializers import DeviceSerializer
from drive.models import Drive


@api_view(['GET'])
def get_list(request):
    if request.method == 'GET':
        return HttpResponse(serializers.serialize('json', Device.objects.all()))

    return HttpResponse(status=400)


@api_view(['POST'])
def create(request):
    if request.method == 'POST':
        if not request.user.is_superuser:
            return HttpResponse(status=403)

        print(request.user)
        name = "쿼카 #{}".format(random.randrange(1, 10000))
        while len(Device.objects.filter(name=name)) > 0:
            name = "쿼카 #{}".format(random.randrange(1, 10000))
        device = Device(name=name)
        device.save()
        return HttpResponse(status=200)

    return HttpResponse(status=400)


@api_view(['DELETE'])
def delete(request, pk):
    if request.method == 'DELETE':
        if not request.user.is_superuser:
            return HttpResponse(status=403)

        device = get_object_or_404(Device, pk=pk)
        device.delete()
        return HttpResponse(status=200)

    return HttpResponse(status=400)


@api_view(['POST'])
def update(request, pk):
    if request.method == 'POST':
        serialize = DeviceSerializer(data=request.data)
        if serialize.is_valid():
            device = get_object_or_404(Device, pk=pk)

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

    return HttpResponse(status=400)


@api_view(['POST'])
def drive(request, pk):
    if request.method == 'POST':
        if request.user.is_anonymous:
            return HttpResponse(status=403)

        device = get_object_or_404(Device, pk=pk)

        if device.using:
            return HttpResponse(status=403)

        drv = Drive(user=request.user, device=device)
        drv.save()

        device.using = True
        device.save()

        return JsonResponse({'pk': drv.pk})

    return HttpResponse(status=400)
