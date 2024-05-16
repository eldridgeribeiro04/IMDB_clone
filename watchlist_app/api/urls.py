from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.WatchListAV.as_view(), name='movie-list'),
    path("movie/<int:pk>/", views.WatchDetailAV.as_view(), name="movie-detail"),
    path("platforms/", views.StreamPlatformListAV.as_view(), name="platforms"),
    path("stream/<int:pk>/", views.StreamPlatformDetailAV.as_view(), name="stream-detail"),

]
