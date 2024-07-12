from django.shortcuts import render
from watchlist_app.models import WatchList, StreamPlatform, Review
from django.http import JsonResponse
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin 
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import AdminOrReadOnly,permission, isDataOwner, isDataOwnerWhenUpdate, AuthorizeCreate, SpecialPermission, SpecialPermission1
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from watchlist_app.api.throttle import AddReviewThrottle, UpdateReviewThrottle
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend,OrderingFilter
from rest_framework import filters
from watchlist_app.api.pagination import newPagination, offsetPagination, cursorPagination
from rest_framework import mixins
from watchlist_app.api.authentication import MyTokenAuthentication
from rest_framework.authentication import authenticate

class GetReviewsByDjangOFilterBackend(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.OrderingFilter]
    # filterset_fields = ['rating', 'reviewer__username']
    # search_fields = ['rating', 'reviewer__username']
    ordering_fields = ['rating', 'reviewer__username']

class GetReviewsByParameters(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        return Review.objects.filter(reviewer__username=username)

class GetReviews(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    def get_queryset(self):
        username = self.kwargs.get("username")

        return Review.objects.filter(reviewer__username=username)

class WatchListVS(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [SpecialPermission]
    

    def create(self, request, *args, **kwargs):
        request.data["adder"] = request.user.id
        # stream = StreamPlatform.objects.get(id=request.data["stream"])
        # stream_serializer = StreamPlatformSerializer(stream)
        # request.data["stream"] = stream_serializer
            
        serializer = WatchListSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response({"error":serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        
    def perform_create(self, serializer):
        self.user = self.request.user
        # self.request.data["adder"] = self.request.user.id
        serializer.save(adder=self.user.id)
        
        # if (serializer.is_valid()):
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     print(serializer.errors)
        #     return Response({"error":serializer.errors}, status=status.HTTP_404_NOT_FOUND)

class AddWatchList(generics.CreateAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(adder=user)

# StreamPlatform list with generics.ListAPIView
# Add the pagination_class into the class
# Check if it only works for generics, not viewsets
class StreamingPlatformListVS(generics.ListAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    pagination_class = newPagination

class StreamingPlatformListOffsetVS(generics.ListAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    pagination_class = offsetPagination

class StreamingPlatformListCursorVS(generics.ListAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    pagination_class = cursorPagination

class StreamingPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

    permission_classes = [SpecialPermission]
    pagination_class = newPagination

    # def create(self, request):
    #     user = request.user
    #     request.data["reviewer"]  = user
    #     serializer = StreamPlatformSerializer(data=request.data)
    #     if (serializer.is_valid()):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        # get the user
        # set it into the data of the request
        # set the serializer, then save it

# class StreamingPlatformVS(generics.ListCreateAPIView):
#     serializer_class = StreamPlatformSerializer
#     queryset = StreamPlatform.objects.all()
#     # authentication_classes = [TokenAuthentication]
#     permission_classes = [SpecialPermission]

# class StreamingPlatformCreate(generics.CreateAPIView):
#     serializer_class = StreamPlatformSerializer
#     queryset = StreamPlatform.objects.all()

class StreamingPlatformUpdate(generics.UpdateAPIView):
    serializer_class = StreamPlatformSerializer
    queryset = StreamPlatform.objects.all()
class StreamingPlatformDestroy(generics.DestroyAPIView):
    serializer_class = StreamPlatformSerializer
    queryset = StreamPlatform.objects.all()


class ReviewVS(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [MyTokenAuthentication]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [isDataOwnerWhenUpdate]

class AddReviewVS(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    throttle_classes = [AddReviewThrottle]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(reviewer=user)

class UpdateReviewVS(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    throttle_classes = [UpdateReviewThrottle]

    def perform_save(self, serializer):
        user = self.request.user
        serializer.save(reviewer=user)

class DeleteReviewVS(generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "delete_review"

class WatchListReview(generics.ListCreateAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)
    
    def perform_save(self, serializer):
        pk = self.kwargs['pk']
        watchlist = WatchList.objects.get(pk=pk)
        reviewer = self.request.user
        
        review_queryset = Review.objects.filter(watchlist=watchlist, reviewer=reviewer)
        serializer.save(watchlist=watchlist, reviewer=reviewer)



class AddReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    authentication_classes = [MyTokenAuthentication]
    #authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Review.objects.all()

    def perform_save(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        reviewer = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, reviewer=reviewer)

    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        watchLists = WatchList.objects.all()
        watchListSerializer = WatchListSerializer(data={"name":watchlist.name})
        reviewer = self.request.user or self.request.auth.user
        watchlist.average_rating = round(watchlist.calculate_average_rating(), 2)
        watchlist.number_rating = watchlist.calculate_total_rating()  

        if (watchListSerializer.is_valid()):
            watchListSerializer.save(watchlist=watchlist)
        serializer.save(watchlist=watchlist, reviewer=reviewer)