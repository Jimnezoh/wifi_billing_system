from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from wifi.serializers import WifiAccessCodeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_wifi_code(request):
    try:
        serializer = WifiAccessCodeSerializer(data=request.data)
        if serializer.is_valid():
            access_code = serializer.save()
            return Response({
                "message": "WiFi access code generated successfully",
                "code": access_code.code,
                "expires_at": access_code.expires_at
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"detail": f"Server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )