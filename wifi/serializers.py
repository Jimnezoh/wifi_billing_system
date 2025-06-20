from rest_framework import serializers
from .models import WifiAccessCode
from users.models import User

class WifiAccessCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = WifiAccessCode
        fields = ['phone_number', 'full_name', 'amount_paid', 'duration_minutes', 'code', 'expires_at']
        read_only_fields = ['code', 'expires_at']

    def create(self, validated_data):
        phone = validated_data.pop('phone_number')
        name = validated_data.pop('full_name', None)

        # Normalize phone_number format
        phone = phone.strip().replace(" ", "").replace("+", "")
        if phone.startswith("07") and len(phone) == 10:
            phone = "254" + phone[1:]

        user, created = User.objects.get_or_create(phone_number=phone, defaults={"full_name": name, "role": "client"})

        access_code = WifiAccessCode.objects.create(user=user, **validated_data)
        return access_code
