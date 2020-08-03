from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser
from customAuth import serializers


class CustomTokenObtainPairView(TokenObtainPairView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    parser_classes = [JSONParser]
    serializer_class = serializers.CustomTokenObtainPairSerializer
