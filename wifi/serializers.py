from rest_framework import serializers
from .models import WifiAccessCode
from users.models import User

from .utils import send_sms

class WifiAccessCodeSerializer(serializers.Serializer):
    
    # declaring the fields manually so as to be included in validated_data passed in model.


    phone_number = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True, required=False)
    amount_paid = serializers.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = serializers.IntegerField()

    code = serializers.CharField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)

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

        user, created = User.objects.get_or_create(phone_number=phone, defaults={"full_name": name or "Anonymous", "role": "client"})

        access_code = WifiAccessCode.objects.create(user=user, **validated_data)

        #send SMS notification

        message = f"Dear customer, your WiFi access code is {access_code.code}. It will expire at {access_code.expires_at}."
        send_sms(phone, message)

        
        return access_code
