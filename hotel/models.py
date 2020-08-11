from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def get_hotel_image_upload_path(instance, filename):
    return "hotel/files/hotels/{}/image/{}".format(instance.id, filename)


CITY_TYPE_CHOICES = [
    ('international', 'international'),
    ('domestic', 'domestic'),
]

FACILITY_TYPE_CHOICES = [
    ('customer_services', 'customer_services'),
    ('public_spaces', 'public_spaces'),
    ('shopping', 'shopping'),
    ('transportation', 'transportatio'),
    ('sports', 'sports'),
    ('housekeeping', 'housekeeping'),
    ('hotel_services', 'hotel_services'),
    ('activities', 'activities'),
    ('misc', 'misc'),
    ('entertainment', 'entertainment'),
    ('foods_and_drinks', 'foods_and_drinks'),
    ('business_meetings', 'business_meetings'),
]


class City(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(choices=CITY_TYPE_CHOICES, max_length=64)


class Hotel(models.Model):

    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    # city = models.ForeignKey(
    #     to=City,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )

    city = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )

    address = models.TextField(
        max_length=512,
        null=True,
        blank=True,
    )
    instructions = models.TextField(
        max_length=2048,
        null=True,
        blank=True,
    )

    stars = models.PositiveSmallIntegerField(
        default=3,
        validators=[MaxValueValidator(5)],
        null=True,
        blank=True,
    )

    image1 = models.ImageField(
        upload_to=get_hotel_image_upload_path,
        null=True,
        blank=True,
    )
    image2 = models.ImageField(
        upload_to=get_hotel_image_upload_path,
        null=True,
        blank=True,
    )

    image3 = models.ImageField(
        upload_to=get_hotel_image_upload_path,
        null=True,
        blank=True,
    )

    image4 = models.ImageField(
        upload_to=get_hotel_image_upload_path,
        null=True,
        blank=True,
    )

    image5 = models.ImageField(
        upload_to=get_hotel_image_upload_path,
        null=True,
        blank=True,
    )

    image6 = models.ImageField(
        upload_to=get_hotel_image_upload_path,
        null=True,
        blank=True,
    )

    loc_x = models.DecimalField(
        max_digits=18,
        decimal_places=16,
        default=-54.041680317979825,
    )
    loc_y = models.DecimalField(
        max_digits=18,
        decimal_places=16,
        default=39.10622758640926,
    )

    price = models.PositiveIntegerField(
        default=1626321
    )


class Facility(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
    )

    type = models.CharField(
        max_length=64,
        choices=FACILITY_TYPE_CHOICES,
    )

    description = models.CharField(
        max_length=128
    )


class Breadcrumb(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
    )

    description = models.CharField(
        max_length=128
    )


class Room(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=128,
    )

    has_breakfast = models.BooleanField(
        default=False,
    )

    adults_number = models.PositiveSmallIntegerField(
        default=0,
    )

    children_number = models.PositiveSmallIntegerField(
        default=0
    )

    total = models.PositiveIntegerField(
        default=200000,
        blank=True,
        null=True,
    )

