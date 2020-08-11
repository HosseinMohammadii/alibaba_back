from rest_framework import serializers


from hotel.models import Hotel, Facility, Room, City, Breadcrumb, FACILITY_TYPE_CHOICES


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = [
            'id',
            'name', 'type',
        ]


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = [
            'id',
            'hotel', 'name', 'has_breakfast', 'adults_number', 'children_number', 'total'
        ]
        extra_kwargs = {
            'total': {
                'required': False,
            }
        }


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = [
            'id',
            'hotel', 'type', 'description',
        ]


class HotelSerializer(serializers.ModelSerializer):

    _id = serializers.IntegerField(source='id', read_only=True)
    facilities = serializers.SerializerMethodField()
    rooms = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    breadcrumbs = serializers.SerializerMethodField()
    loc = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            '_id',
            'name', 'city', 'address', 'instructions',
            'images',
            'facilities',
            'rooms',
            'breadcrumbs',
            'loc',
            'price',
            'stars',
        ]

    def get_facilities(self, obj):
        facility_types = [facility_type[0] for facility_type in FACILITY_TYPE_CHOICES]
        res = dict()

        for facility_type in facility_types:
            res[facility_type] = Facility.objects.filter(hotel=obj, type=facility_type).values_list('description', flat=True)

        return res

    def get_rooms(self, obj):
        qs = Room.objects.filter(hotel=obj)
        return RoomSerializer(qs, many=True).data

    def get_images(self, obj):
        request = self.context.get("request")
        images = []
        for i in range(1, 7):
            image = getattr(obj, 'image'+str(i))
            if image:
                images.append(request.build_absolute_uri(image.url))

        return images

    def get_breadcrumbs(self, obj):
        res = Breadcrumb.objects.filter(hotel=obj).values_list('description', flat=True)
        return res

    def get_loc(self, obj):
        return {'x': obj.loc_x, 'y': obj.loc_y}
