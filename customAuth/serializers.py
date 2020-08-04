from django.contrib.auth import get_user_model
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
import django.contrib.auth.password_validation as validators

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        attrs[self.username_field] = attrs[self.username_field].lower()

        try:
            user = User.objects.get(email=attrs[self.username_field])
            if not user.check_password(attrs['password']):
                raise AuthenticationFailed({"detail": "Password is incorrect."})

        except User.DoesNotExist:
            raise AuthenticationFailed({"detail": "No user found with this email."})

        data = super().validate(attrs)
        return data


def validate_user_password(password):
    try:
        # validate the password and catch the exception
        validators.validate_password(password)

    # the exception raised here is different than serializers.ValidationError
    except exceptions.ValidationError as e:
        raise serializers.ValidationError(e.messages)


def validate_email(email):
    qs = User.objects.filter(email__iexact=email)
    if qs.exists():
        raise serializers.ValidationError(_("User with this email already exists"))


def validate_phone_number(phone):
    try:
        int(phone)
    except ValueError:
        raise serializers.ValidationError(_("Phone number should be number only"))


class UserRegisterSerializer(serializers.ModelSerializer):
    token_response = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'phone_number',
            'token_response',
        ]

        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'required': True}
        }

    def get_token_response(self, obj):
        data = {}
        refresh = RefreshToken.for_user(obj)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    def validate_password(self, value):
        validate_user_password(value)
        return value

    def validate_email(self, value):
        validate_email(value)
        return value.lower()

    def validate_phone_number(self, value):
        validate_phone_number(value)
        return value

    def create(self, validated_data):
        user_obj = User(
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            user_type=1,  # Only student can register with serializer
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj

