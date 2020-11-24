from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'birth']


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(allow_blank=False, max_length=100)
