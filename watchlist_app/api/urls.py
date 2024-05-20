from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('platform', views.StreamPlatformVS, basename='streamplatform-detail'),

urlpatterns = [
    path("list/", views.WatchListAV.as_view(), name='movie-list'),
    path("<int:pk>/", views.WatchDetailAV.as_view(), name="movie-detail"),
    
    path('', include(router.urls)),
    
    # path("platforms/", views.StreamPlatformListAV.as_view(), name="platforms"),
    # path("stream/<int:pk>/", views.StreamPlatformDetailAV.as_view(), name="streamplatform-detail"),
    
    # path("reviews/", views.ReviewList.as_view(), name="review-list"),
    # path("reviews/<int:pk>/", views.ReviewDetail.as_view(), name="review-detail"),
    
    path("stream/<int:pk>/review-create/", views.ReviewCreate.as_view(), name="review-create"),
    path("stream/<int:pk>/review/", views.ReviewList.as_view(), name="review-list"),
    path("stream/review/<int:pk>/", views.ReviewDetail.as_view(), name="review-detail"),
]
