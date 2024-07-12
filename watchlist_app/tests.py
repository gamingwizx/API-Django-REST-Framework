from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token 
from django.urls import reverse
from watchlist_app.models import StreamPlatform, Review, WatchList
from rest_framework import status
class TestStreamPlatform(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.token = Token.objects.get(user__username=self.user)
        # self.username = "testuser"
        # self.password = "testpassword"
        # self.user = User.objects.create(username=self.username)
        # self.user.set_password(self.password)
        # self.user.save()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        # self.client.login(username=self.user.username, password=self.user.password)
        self.streamingPlatform = StreamPlatform.objects.create(name="Crunchyroll", about="Stream Platform", website="https://www.crunchyroll.com")

    def test_create_stream_platform(self):

        data = {
            "name": "Crunchyroll5",
            "about": "Crunchyrol3",
            "website": "https://crunchyroll.com/"
        }

        response = self.client.post(reverse("StreamingPlatform-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_stream_platform(self):
        response = self.client.get(reverse("StreamingPlatform-list"))
   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_stream_platform(self):
        print(self.streamingPlatform.id)
        response = self.client.get(reverse("StreamingPlatform-detail", args=(self.streamingPlatform.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_stream_platform(self):
        data = {
            "name": "updated - Crunchyroll5",
            "about": "Crunchyrol3",
            "website": "https://crunchyroll.com/"
        }
        response = self.client.put(reverse("StreamingPlatform-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_stream_platform(self):
        response = self.client.delete(reverse("StreamingPlatform-detail", args=(self.streamingPlatform.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestReviewPlatform(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.streamingPlatform = StreamPlatform.objects.create(name="Crunchyroll", about="Stream Platform", website="https://www.crunchyroll.com")
        self.watchlist = WatchList.objects.create(name="Fallout", adder=self.user, stream=self.streamingPlatform, description="Fallout description", isExist=True)
        self.review = Review.objects.create(rating=5, reviewer=self.user, description="Fallout description", active=True, watchlist=self.watchlist)

    def test_create_review(self):
        data = {
            "rating": 3,
            "description": "This is a really good movie",
            "active": True,
            "watchlist": self.watchlist
        }
        response = self.client.post(reverse("create-review", args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_get_all_review(self):
        response = self.client.get(reverse("review-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_watchlist_review(self):
        response = self.client.get(reverse("watchlist-review", args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_review(self):
        response = self.client.delete(reverse("review-detail", args=(self.review.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_update_review(self):
        data = {
            "rating": 3,
            "description": "This is a really good movie",
            "active": True,
            "watchlist": self.watchlist
        }
        response = self.client.put(reverse("review-detail", args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestWatchListPlatform(APITestCase): 
    # Create, Update, Delete, Get and Get all WatchList
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="testpassword")
        self.token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.streamingPlatform = StreamPlatform.objects.create(name="Crunchyroll", about="Stream Platform", website="https://www.crunchyroll.com")
        self.watchlist = WatchList.objects.create(name="Fallout", adder=self.user, stream=self.streamingPlatform, description="Fallout description", isExist=True)

    def test_create_watchlist(self):
        data = {
            "name": "Fallout Remastered",
            "description": "A movie made out of a game",
            "isExist": True,
            "number_rating": 0,
            "average_rating": 0.0,
            "stream": self.streamingPlatform.id
        }

        response = self.client.post(reverse("WatchListVS-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_watchlist(self):
        data = {
            "name": "Fallout Remastered",
            "description": "A movie made out of a game",
            "isExist": True,
            "number_rating": 0,
            "average_rating": 0.0,
            "stream": self.streamingPlatform.id
        }

        response = self.client.put(reverse("WatchListVS-detail", args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_watchlist(self):
        response = self.client.delete(reverse("WatchListVS-detail", args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_watchlist(self):
        response = self.client.get(reverse("WatchListVS-detail", args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_watchlist(self):
        response = self.client.get(reverse("WatchListVS-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestStreamingPlatformPlatform(APITestCase): 
    # Create, Update, Delete, Get and Get all StreamingPlatform
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="testpassword")
        self.token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.streamingPlatform = StreamPlatform.objects.create(name="Crunchyroll", about="Stream Platform", website="https://www.crunchyroll.com")

    def test_create_StreamingPlatform(self):
        data = {
            "name": "Crunchyroll7",
            "about": "Crunchyrol3",
            "website": "https://crunchyroll.com/"
        }

        response = self.client.post(reverse("StreamingPlatform-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_StreamingPlatform(self):
        data = {
            "name": "Crunchyroll7",
            "about": "Crunchyrol3",
            "website": "https://crunchyroll.com/"
        }

        response = self.client.put(reverse("StreamingPlatform-detail", args=(self.streamingPlatform.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_StreamingPlatform(self):
        response = self.client.delete(reverse("StreamingPlatform-detail", args=(self.streamingPlatform.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_StreamingPlatform(self):
        response = self.client.get(reverse("StreamingPlatform-detail", args=(self.streamingPlatform.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_StreamingPlatform(self):
        response = self.client.get(reverse("StreamingPlatform-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
