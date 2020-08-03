from rest_framework import serializers

from hotel.models import Hotel, Facility, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'id',
            'hotel', 'name', 'has_breakfast', 'adults_number', 'children_number',
        ]


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = [
            'id',
            'hotel', 'type', 'description',
        ]


class HotelSerializer(serializers.ModelSerializer):

    facilities = serializers.SerializerMethodField()
    rooms = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            'id',
            'name', 'city', 'address', 'instructions',
            'image1', 'image2', 'image3', 'image4', 'image5', 'image6',
            'facilities',
            'rooms',
        ]

    def get_facilities(self, obj):
        qs = Facility.objects.filter(hotel=obj)
        return FacilitySerializer(qs, many=True).data

    def get_rooms(self, obj):
        qs = Room.objects.filter(hotel=obj)
        return RoomSerializer(qs, many=True).data
