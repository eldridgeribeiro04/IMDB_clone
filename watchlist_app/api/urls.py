from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.WatchListAV.as_view(), name='movie-list'),
    path("<int:pk>/", views.WatchDetailAV.as_view(), name="movie-detail"),
    path("platforms/", views.StreamPlatformListAV.as_view(), name="platforms"),
    path("stream/<int:pk>/", views.StreamPlatformDetailAV.as_view(), name="streamplatform-detail"),
    
    path("reviews/", views.ReviewtList.as_view(), name="review-list"),
    path("reviews/<int:pk>/", views.ReviewDetail.as_view(), name="review-detail"),
]
