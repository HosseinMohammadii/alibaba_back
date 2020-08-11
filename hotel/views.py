import binascii
import io
import defusedxml
from django.db.models import Count, Sum
from django.shortcuts import render
import xml
from rest_framework import generics
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.parsers import BaseParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_xml.renderers import XMLRenderer
# from rest_framework_xml.parsers import XMLParser
from rest_framework.renderers import BrowsableAPIRenderer
from django.utils.encoding import smart_text
from rest_framework import renderers

from hotel.serializers import HotelSerializer, RoomSerializer, FacilitySerializer, CitySerializer
from hotel.models import Hotel, Room, Facility, City

from customAuth.permissions import IsAuthenticated, UserIsHotelOwner
from hotel import permissions

from hotel.parsers import XMLParser


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
# @renderer_classes([JSONRenderer])
@renderer_classes([JSONRenderer])
@api_view(['POST'])
def convert_xml_to_json(request, format=None):
    # print(request.META['CONTENT_TYPE'])
    # print(request.body)
    # print(request)
    f = io.StringIO(request.body.decode('utf-8'))
    xml_parser = XMLParser()
    data = xml_parser.parse(stream=f)

    # print(data)
    # data = XMLRenderer().render(data=data)
    # data = JSONRenderer().render(data=data)

    # print(data)
    return Response(
        data=data,
        status=200,
        # content_type='application/json',
    )


@parser_classes([XMLParser])
@renderer_classes([JSONRenderer])
@api_view(['POST'])
def hotel_search(request, format=None):
    f = io.StringIO(request.body.decode('utf-8'))
    xml_parser = XMLParser()
    request_data = xml_parser.parse(stream=f)

    qs = Hotel.objects.none()
    city = request_data.get('city', None)
    guests = request_data.get('guests', None)
    adults_number = None
    children_number = None
    if guests is not None:
        adults_number = guests.get('parents', None)
        children_number = guests.get('children', None)

    if city is not None:
        qs |= Hotel.objects.filter(city__icontains=city)
    else:
        qs |= Hotel.objects.all()

    if adults_number is not None:
        temp_qs = qs
        temp = temp_qs.annotate(sum_adults=Sum('room__adults_number'))
        temp_hotel_ids = temp.filter(sum_adults__gte=adults_number).values_list('id', flat=True)
        qs = qs.filter(id__in=temp_hotel_ids)

    if children_number is not None:
        temp_qs = qs
        temp = temp_qs.annotate(sum_children=Sum('room__children_number'))
        temp_hotel_ids = temp.filter(sum_children__gte=children_number).values_list('id', flat=True)
        qs = qs.filter(id__in=temp_hotel_ids)

    qs = qs.distinct()
    serializer = HotelSerializer(qs, many=True, context={'request': request})

    # print(data)
    # data = XMLRenderer().render(data=data)
    # data = JSONRenderer().render(data=data)

    # print(data)
    return Response(
        data={'hotels': serializer.data},
    )


@parser_classes([XMLParser])
@renderer_classes([JSONRenderer])
@api_view(['POST'])
def hotel_rooms_search(request, format=None):

    f = io.StringIO(request.body.decode('utf-8'))
    xml_parser = XMLParser()
    request_data = xml_parser.parse(stream=f)

    qs = Hotel.objects.none()
    guests = request_data.get('guests', None)
    adults_number = None
    children_number = None
    if guests is not None:
        adults_number = guests.get('parents', None)
        children_number = guests.get('children', None)

    # if id is not None:
    #     qs |= Hotel.objects.filter(city__icontains=city)
    # else:
    #     qs |= Hotel.objects.all()

    if adults_number is not None:
        temp_qs = qs
        temp = temp_qs.annotate(sum_adults=Sum('room__adults_number'))
        temp_hotel_ids = temp.filter(sum_adults__gte=adults_number).values_list('id', flat=True)
        qs = qs.filter(id__in=temp_hotel_ids)

    if children_number is not None:
        temp_qs = qs
        temp = temp_qs.annotate(sum_children=Sum('room__children_number'))
        temp_hotel_ids = temp.filter(sum_children__gte=children_number).values_list('id', flat=True)
        qs = qs.filter(id__in=temp_hotel_ids)

    qs = qs.distinct()
    serializer = HotelSerializer(qs, many=True, context={'request': request})

    # print(data)
    # data = XMLRenderer().render(data=data)
    # data = JSONRenderer().render(data=data)

    # print(data)
    return Response(
        data={'hotels': serializer.data},
    )


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


class RoomListByHotelAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    renderer_classes = [JSONRenderer, ]

    def get_queryset(self):
        id = self.kwargs['id']
        try:
            hotel = Hotel.objects.get(id=id)
            qs = Room.objects.filter(hotel=hotel)
        except Hotel.DoesNotExist:
            qs = Room.objects.none()

        return qs
