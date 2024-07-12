from login_app.api.serializers import RegisterSerializer 
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from watchlist_app.api.permissions import isDataOwnerWhenUpdate
from watchlist_app.models import Review
from watchlist_app.api.serializers import ReviewSerializer
from login_app.api.tokens import get_jwt_tokens
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from login_app.MyTokenAuthentication import MyTokenAuthentication
from rest_framework.authentication import TokenAuthentication

@api_view(['POST', ])
@authentication_classes([TokenAuthentication])
def logout_view(request):
    if (request.method == "POST"):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class RegisterUser(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=self.request.data, context={'request': request})
        data = {}
        if (serializer.is_valid(raise_exception=True)):
            account = serializer.save()
            token = Token.objects.get(user=account).key
            data['response'] = "Registration successful"
            data['username'] = serializer.data['username']
            data['email'] = serializer.data['email']
            data['token'] = token



        return Response(data, status=status.HTTP_201_CREATED)

        
    # def create(self):
    #     new_user = User.objects.create(data=self.request.data)

    #     password = self.validated_data['passwords']
    # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    # def create_auth_token(sender, instance=None, created=False, **kwargs):
    #     if created:
    #         Token.objects.create(user=instance)

class LoginJWT(APIView):
    def post(self, request):
        user = authenticate(username=self.request.data["username"], password=self.request.data["password"])
        if user is not None:
            tokens = get_jwt_tokens(user)
            return Response({"Success": tokens}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
class testRegister(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
