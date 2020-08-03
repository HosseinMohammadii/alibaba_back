from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_xml.parsers import XMLParser

from hotel.serializers import HotelSerializer, RoomSerializer, FacilitySerializer,  CitySerializer
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

@renderer_classes([XMLRenderer])
@api_view(['GET'])
def get_international_cities(request, format=None):
    qs = City.objects.filter(type='international')
    data = qs.values_list('name', flat=True)
    return Response(
        data
    )


class PublicHotelListAPIView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class PublicHotelRetrieveAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


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




