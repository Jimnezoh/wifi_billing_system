from django.urls import path
from wifi.views import generate_wifi_code

urlpatterns = [
    path('generate-wifi-code/', generate_wifi_code, name='generate_wifi_code'),
]
