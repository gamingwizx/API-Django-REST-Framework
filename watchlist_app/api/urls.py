from django.urls import path,include
from rest_framework.routers import DefaultRouter 
# from watchlist_app.api.views import movie_list, movie_detail
# from watchlist_app.api.views import (WatchListVS, StreamingPlatformViewSet, ReviewList, Reviews,ReviewWatchList,ReviewCreate, )
from watchlist_app.api.views import (WatchListVS, StreamingPlatformVS, ReviewVS, WatchListReview, AddReview, AddReviewVS, UpdateReviewVS, DeleteReviewVS, GetReviews,GetReviewsByParameters, GetReviewsByDjangOFilterBackend, StreamingPlatformListVS, StreamingPlatformListOffsetVS, StreamingPlatformListCursorVS, AddWatchList)
router = DefaultRouter()
router.register(r'streams', StreamingPlatformVS, basename='StreamingPlatform')
router.register(r'list', WatchListVS, basename='WatchListVS')
router.register(r'reviews', ReviewVS, basename='review')
urlpatterns = [
    # path("streams/", StreamingPlatformVS.as_view(), name="streams"),
    path('AddWatchList/', StreamingPlatformListVS.as_view(), name='add-watchlist'),
    path('streaming-pagination/', StreamingPlatformListVS.as_view(), name='streaming-pagination'),
    path('streaming-pagination-offset/', StreamingPlatformListOffsetVS.as_view(), name='streaming-pagination-offset'),
    path('streaming-pagination-cursor/', StreamingPlatformListCursorVS.as_view(), name='streaming-pagination-cursor'),
    path('<int:pk>/review', WatchListReview.as_view(), name='watchlist-review'),
    path('get-all-reviews/<str:username>/', GetReviews.as_view(), name='watchlist-review'),
    path('get-all-reviews-backend/', GetReviewsByDjangOFilterBackend.as_view(), name='watchlist-backend'),
    path('get-all-reviews-params/', GetReviewsByParameters.as_view(), name='watchlist-review'),
    path('<int:pk>/create-review', AddReview.as_view(), name='create-review'),
    path('<int:pk>/delete-review', DeleteReviewVS.as_view(), name="delete-review"),
    path('<int:pk>/add-review', AddReviewVS.as_view(), name="add-review"),
    path('<int:pk>/update-review', UpdateReviewVS.as_view(), name="update-review"),
    # path('test/', test.as_view(), name='test'),
    path('', include(router.urls)),
]
# urlpatterns = [
#     path('', include(router.urls)),
#     path("reviews/", ReviewList.as_view(), name='review-list'),
#     path("reviews/<int:pk>", Reviews.as_view(), name='review'),
#     path("<int:pk>/reviews", ReviewWatchList.as_view(), name='review-watch-list'),
#     path("<int:pk>/review-create", ReviewCreate.as_view(), name='review-watch-create')
# ]