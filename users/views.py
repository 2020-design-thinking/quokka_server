from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import User
from .serializers import UserSerializer


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    return HttpResponse(status=400)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
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


@api_view(['GET'])
def get_details(request, pk):
    if request.method == 'GET':
        user = get_object_or_404(User, pk=pk)
        return JsonResponse({'username': user.username,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'points': user.points,
                             'safety_rate': user.safety_rate})

    return HttpResponse(status=400)
