from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from login_app.api.views import RegisterUser, logout_view, LoginJWT, testRegister

router = DefaultRouter()
urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login-jwt/', LoginJWT.as_view(), name='login-jwt'),
    path('register-jwt/', testRegister.as_view(), name='register-jwt'),
    path('logout/', logout_view, name='logout')
]