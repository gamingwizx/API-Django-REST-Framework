from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate

class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "testpassword",
            "repeat_password": "testpassword" 
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class LogoutTestCase(APITestCase):
    
    def setUp(self):
         self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_login(self):
        data = {
            "username": "testuser",
            "password": "testpassword"
        }

        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_logout(self):
        self.token = Token.objects.get(user__username="testuser")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
