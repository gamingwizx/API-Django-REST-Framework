from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('api/verify/', TokenVerifyView.as_view(), name="token_verify"),
    path('admin/', admin.site.urls),
    path('watchlist/', include('watchlist_app.api.urls')),
    path('account/', include('login_app.api.urls')),
]
