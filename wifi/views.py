from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from wifi.serializers import WifiAccessCodeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_access_code(request):
    serializer = WifiAccessCodeSerializer(data=request.data)
    if serializer.is_valid():
        access_code = serializer.save()
        return Response({
            "message": "Access code generated successfully",
            "code": access_code.code,
            "expires_at": access_code.expires_at
            },
            status=status.HTTP_201_CREATED
        )