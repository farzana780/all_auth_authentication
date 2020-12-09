from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.admin import AccessToken
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import json

from rest_framework.views import APIView

from accountapp.models import CustomUser
from accountapp.serializers import CreateUserSerializer, UserSerializer


@csrf_exempt
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def test(request):
    token = AccessToken.objects.get(token=request.data['token'])
    users = CustomUser.objects.get(id=token.user_id)
    user_serialiser = UserSerializer(users, many=False)
    # json_data = JSONRenderer().render(user_serialiser.data)
    return JsonResponse({'user': user_serialiser.data})


#
# from rest_framework import generics
#
#
# class SignUp(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CreateUserSerializer
#     permission_classes = (IsAuthenticated,)
#
#
from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import requests

from .serializers import CreateUserSerializer


# CLIENT_ID = '4hg70yCJtauX5h8Zd33mgJajJSRFbGMl1S7tZjGw'
# CLIENT_SECRET = 'aZ72QZGI53Ks8gSC4LZARHaQyeN6TLbYWim4Wml7zVr6oGvzp8Kre5cnhCmVCqGuwx1UlBSmAjHCVDqxlusmNwHCBQlgKNiooXH2bASkO84ILUzvYxlbXDKbBsJjeBYU'


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     '''
#     Registers user to the server. Input should be in the format:
#     {"username": "username", "password": "1234abcd"}
#     '''
#     # Put the data from the request into the serializer
#     serializer = CreateUserSerializer(data=request.data)
#     # Validate the data
#     if serializer.is_valid():
#         # If it is valid, save the data (creates a user).
#         serializer.save()
#         # Then we get a token for the created user.
#         # This could be done differentley
#
#         return Response('Successfully Registered')
#     return Response(serializer.errors)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
    'http://127.0.0.1:8000/o/token/',
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id':  request.data['client_id'],
            'client_secret': request.data['client_secret'],
        },
    )
    return Response(r.json())


