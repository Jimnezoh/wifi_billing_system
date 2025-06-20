from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers


class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

def validate(self, attrs):
    phone_number = attrs.get('phone_number')
    password = attrs.get('password')

# the custom authentication logic now comes in---------

    user = authenticate(phone_number=phone_number, password=password)

    if user is None:
            raise serializers.ValidationError("No active account found with the given credentials")

    if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

    data = super().get_token(user)
    return {
        'refresh': str(data),
        'access': str(data.access_token),
    }
