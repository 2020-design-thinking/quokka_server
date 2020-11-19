from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser

from devices.models import Device
from drive.models import Drive
from judge.models import DrivingImage
from judge.serializers import DrivingImageSerializer

from judge.tasks import judge_image


class JudgeViewSet(viewsets.ModelViewSet):

    serializer_class = DrivingImageSerializer
    parser_classes = (MultiPartParser,)

    def image(self, request):
        if request.user.is_anonymous:
            return HttpResponse(status=403)

        if request.user.last_drive is None:
            return HttpResponse(status=400)

        drive = request.user.last_drive

        serializer = DrivingImageSerializer(data=request.data)

        if not serializer.is_valid():
            return HttpResponse(status=400)

        driving_img = DrivingImage(drive=drive, image=serializer.validated_data.get('image'))
        driving_img.save()

    def image_test(self, request):
        if request.user.is_anonymous:
            return HttpResponse(status=403)

        serializer = DrivingImageSerializer(data=request.data)

        drive = Drive(driver=request.user, device=Device.objects.all()[0])
        drive.save()

        if not serializer.is_valid():
            return HttpResponse(status=400)

        driving_img = DrivingImage(drive=drive, image=serializer.validated_data.get('image'))
        driving_img.save()

        judge_image.delay(driving_img.pk)

        return HttpResponse(status=200)
