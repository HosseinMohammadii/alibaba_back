from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def get_hotel_image_upload_path():
    pass


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
    city = models.CharField(
        max_length=128,
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


class Facility(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
    )

    type = models.CharField(
        max_length=64,
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

