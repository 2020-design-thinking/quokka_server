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

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            login_result = authenticate(username=serializer.data['id'], password=serializer.data['pw'])

            if login_result:
                return HttpResponse(status=200)

            return HttpResponse(status=401)

        return HttpResponse(status=400)
