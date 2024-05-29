from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework import filters
# from rest_framework import mixins
# from rest_framework.decorators import api_view

from rest_framework_simplejwt.tokens import RefreshToken

from watchlist_app.models import WatchList, StreamPlatform, Reviews
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewsSerializer
from watchlist_app.api.permissions import IsAdminOrReadOnly, ReviewUserOrReadOnly
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from watchlist_app.api.pagination import WatchListPagination, WatchListLOPagination

from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend


class UserReview(generics.ListAPIView):
    # throttle_classes = [ReviewListThrottle]
    
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]
    
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Reviews.objects.filter(author__username=username)
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Reviews.objects.filter(author__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Reviews.objects.filter(author=review_user, watchlist=movie)
        
        if review_queryset.exists():
            raise exceptions.PermissionDenied("You have already reviewed this movie")
        
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data["rating"]
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data["rating"])/2
            
        movie.number_rating = movie.number_rating + 1
        movie.save()
        
        serializer.save(watchlist=movie, author=review_user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewsSerializer
    
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ReviewListThrottle]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author__username', 'watchlist__title']

    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reviews.objects.filter(watchlist=pk)
        
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "review-detail"
    
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [ReviewUserOrReadOnly]


# class ReviewDetail(mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    generics.GenericAPIView):
    
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewsSerializer
    
#     def get(self, request, pk, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, pk, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, pk, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class ReviewtList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewsSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListLOPagination
        
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['title', 'platform__name']

    # permission_classes = [IsAuthenticated]
    

class WatchListAV(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        watchlist = WatchList.objects.all()
        serializer = WatchListSerializer(watchlist, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class WatchDetailAV(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
        
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)
    
    def put(self, request, pk):
        watchList = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(watchList,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        watchList = WatchList.objects.get(pk=pk)
        watchList.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    
    
# class StreamPlatformVS(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     def destroy(self, request, pk):
#         stream_platform = StreamPlatform.objects.get(pk=pk)
#         stream_platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

    
class StreamPlatformListAV(APIView):
    
    def get(self, request):
        stream_platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(stream_platforms, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
class StreamPlatformDetailAV(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            stream_platform = StreamPlatform.objects.get(pk=pk)
        
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(stream_platform, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        stream_platform = StreamPlatform.objects.get(pk=pk)
        stream_platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        


# @api_view(["GET", "POST"])
# def movie_list(request):
#     if request.method == "GET":
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(["GET" ,"PUT", "DELETE"])
# def movie_detail(request, pk):
#     if request.method == "GET":
        
#         try:
#             movie = Movie.objects.get(pk=pk)
        
#         except Movie.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == "PUT":
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     if request.method == "DELETE":
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)