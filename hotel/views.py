import binascii
import io

from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.parsers import BaseParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_xml.parsers import XMLParser
from rest_framework.renderers import BrowsableAPIRenderer
from django.utils.encoding import smart_text
from rest_framework import renderers

from hotel.serializers import HotelSerializer, RoomSerializer, FacilitySerializer, CitySerializer
from hotel.models import Hotel, Room, Facility, City

from customAuth.permissions import IsAuthenticated, UserIsHotelOwner
from hotel import permissions


# @api_view(['GET'])
# def get_domestic_cities(request, format=None):
#     qs = City.objects.filter(type='domestic')
#     serializer = CitySerializer(qs, many=True)
#     return Response(
#         serializer.data
#     )


@api_view(['GET'])
def get_domestic_cities(request, format=None):
    qs = City.objects.filter(type='domestic')
    data = qs.values_list('name', flat=True)
    return Response(
        data
    )


# @api_view(['GET'])
# def get_international_cities(request, format=None):
#     qs = City.objects.filter(type='international')
#     serializer = CitySerializer(qs, many=True)
#     return Response(
#         serializer.data
#     )

@renderer_classes([JSONRenderer])
@api_view(['GET'])
def get_international_cities(request, format=None):
    qs = City.objects.filter(type='international')
    data = qs.values_list('name', flat=True)
    return Response(
        data
    )


class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return smart_text(data, encoding=self.charset)


# @parser_classes([PlainTextParser])
# @renderer_classes([PlainTextRenderer])
@parser_classes([XMLParser])
@renderer_classes([JSONRenderer])
@api_view(['POST'])
def convert_xml_to_json(request, format=None):
    # print(request.META['CONTENT_TYPE'])
    # print(request.body)
    # print(request)
    f = io.StringIO(request.body.decode('utf-8'))
    xml_parser = XMLParser()
    obj = xml_parser.parse(stream=f)
    print(obj)
    # data = request.data
    # print(type(data))
    # print(data)
    return Response(
        data=obj,
        status=200,
        # content_type='text/plain',
    )


# class XMLToJSON(APIView):
#     parser_classes = [PlainTextParser]
#     renderer_classes =
#
#     def post(self, request, *args, **kwargs):
#         print(request.META['CONTENT_TYPE'])
#         print(request.META.get('HTTP_CONTENT_TYPE'))
#         # print(request.META['body'])
#         print(request.body)
#         print(request)
#         # print(type(data))
#         # print(data)
#         return Response(
#             data=request.META['CONTENT_TYPE'],
#             status=200,
#             content_type='text/plain'
#         )


class PublicHotelListAPIView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class PublicHotelRetrieveAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class PublicHotelListAPIViewByCity(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_queryset(self):
        city = self.kwargs['city']
        qs = Hotel.objects.filter(city__iexact=city)
        return qs


class OwnerHotelListCreateAPIView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated, UserIsHotelOwner]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            qs = Hotel.objects.filter(owner_id=user.id)
        else:
            qs = Hotel.objects.none()
        return qs


class OwnerHotelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated, UserIsHotelOwner, permissions.IsHotelOwner]


class PublicRoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class PublicRoomRetrieveAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class OwnerRoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated, UserIsHotelOwner]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            qs = Room.objects.filter(hotel__owner_id=user.id)
        else:
            qs = Room.objects.none()
        return qs


class OwnerRoomRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, UserIsHotelOwner, permissions.IsRoomHotelOwner]
