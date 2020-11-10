from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import User
from.serializers import UserSerializer, PasswordSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], serializer_class=AuthTokenSerializer)
    def login(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(username=serializer.validated_data['username'],
                                     email=serializer.validated_data['email'],
                                     password=serializer.validated_data['password'],
                                     first_name=serializer.validated_data['first_name'],
                                     last_name=serializer.validated_data['last_name'],
                                     birth=serializer.validated_data['birth'])
            return HttpResponse(status=201)

        return HttpResponse(status=400)
