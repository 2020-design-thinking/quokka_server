from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'birth']


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'pw']
