from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import User
from .serializers import UserSerializer, TokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializers = {
        'login': AuthTokenSerializer,
        'auth': TokenSerializer,
        'default': UserSerializer
    }
    parser_classes = (FormParser,)
    queryset = User.objects.all()

    def login(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': token.user_id})

    def auth(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = get_object_or_404(Token, key=serializer.validated_data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

    def register(self, request):
        if len(User.objects.filter(username=request.data['username'])) > 0:
            return JsonResponse({'message': 'DUP_ID'}, status=200)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(username=serializer.validated_data['username'],
                                     email=serializer.validated_data['email'],
                                     password=serializer.validated_data['password'],
                                     first_name=serializer.validated_data['first_name'],
                                     last_name=serializer.validated_data['last_name'],
                                     birth=serializer.validated_data['birth'])
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        return JsonResponse({'message': 'UNKNOWN'}, status=400)

    def get_details(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return JsonResponse({'username': user.username,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'points': user.points,
                             'safety_rate': user.safety_rate})

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def cancel_reserve(self, request):
        if request.user.is_anonymous:
            return HttpResponse(status=403)

        if not request.user.is_reserved():
            return JsonResponse({'message': 'NOT_RESERVED'}, status=400)

        request.user.cancel_reserve()

        return JsonResponse({'message': 'SUCCESS'}, status=200)
