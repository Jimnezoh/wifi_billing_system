from rest_framework_simplejwt.views import TokenRefreshView
from users.views import PhoneTokenObtainPairView

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/wifi/', include('wifi.urls')),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', PhoneTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
