from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets

from judge.models import DrivingImage
from judge.serializers import DrivingImageSerializer


class JudgeViewSet(viewsets.ModelViewSet):

    serializer_class = DrivingImageSerializer

    def image(self, request):
        if request.user.is_anonymous:
            return HttpResponse(403)

        if request.user.last_drive is None:
            return HttpResponse(400)

        drive = request.user.last_drive

        serializer = DrivingImageSerializer(data=request.data)

        if not serializer.is_valid():
            return HttpResponse(status=400)

        driving_img = DrivingImage(drive=drive, image=serializer.validated_data.get('image'))
        driving_img.save()
