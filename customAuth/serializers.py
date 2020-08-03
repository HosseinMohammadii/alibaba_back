from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
