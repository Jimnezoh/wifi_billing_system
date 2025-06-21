import africastalking
from django.conf import settings


def send_sms(phone_number, message):
    africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)
    sms = africastalking.SMS

    try:
        response = sms.send(message, [phone_number])
        return response
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return None