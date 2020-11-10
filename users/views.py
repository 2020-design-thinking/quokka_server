from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import User
from.serializers import UserSerializer, PasswordSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], serializer_class=PasswordSerializer)
    def login(self, request):
        return HttpResponse(status=400)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                     last_name=last_name, birth=birth)
        else:
            return HttpResponse(status=400)

        return HttpResponse(status=200)
