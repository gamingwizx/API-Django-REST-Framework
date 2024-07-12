from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf import settings

class StreamPlatform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    about = models.CharField(max_length=500)
    website = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Create your models here.
class WatchList(models.Model):
    name = models.CharField(max_length=50, unique=True)
    stream = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="stream")
    description = models.CharField(max_length=200)
    isExist = models.BooleanField(default=True)
    adder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adder")
    number_rating = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    created = models.DateTimeField(auto_now=True)

    def calculate_total_rating(self):
        return Review.objects.aggregate(Sum("rating", default=1))['rating__sum']
    def calculate_average_rating(self):
        totalRating = Review.objects.aggregate(Sum("rating", default=0))['rating__sum']
        totalReviews = Review.objects.count()

        if (totalRating == 0 or totalReviews == 0):
            return 0
        
        return totalRating / totalReviews


    def __str__(self):
        return self.name
    
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + " - "+ self.watchlist.name

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)