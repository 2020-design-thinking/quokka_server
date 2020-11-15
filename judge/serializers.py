from rest_framework import serializers
from .models import DrivingImage


class DrivingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingImage
        fields = ['image']
