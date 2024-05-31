import token

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password456')
        self.token = Token.objects.get(user__username="user")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name='Netflix',
                                                           about='Stream platform',
                                                           website='www.netflix.com')
        
    def test_stream_platform(self):
        data = {
            'name': 'Netflix',
            'description': 'Streaming',
            'website': 'http://netflix.com',
        }
        
        response = self.client.post(reverse('streamplatform-detail-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-detail-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_delete(self):
        response = self.client.delete(reverse('streamplatform-detail-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_put(self):
        data = {
            'name': 'Netflix- try to change',
            'description': 'Streaming',
            'website': 'http://netflix.com',
        }
        response = self.client.put(reverse('streamplatform-detail-detail', args=(self.stream.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password456')
        self.token = Token.objects.get(user__username="user")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name='Netflix',
                                                           about='Stream platform',
                                                           website='www.netflix.com')
        self.movie = models.WatchList.objects.create(title='Test Movie',
                                                      description='test_description',
                                                      platform=self.stream,
                                                      active=True)
    
    def test_watchlist_create(self):
        data = {
            'title': 'test_title',
            'description': 'test_description',
            'platform': self.stream.id,
            'active': True,
        }
        
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response = self.client.get(reverse('movie-detail', args=(self.movie.id,)))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title, 'Test Movie')
        
        
class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password456')
        self.token = Token.objects.get(user__username="user")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name='Netflix',
                                                           about='Stream platform',
                                                           website='www.netflix.com')
        self.movie = models.WatchList.objects.create(title='Test Movie',
                                                      description='test_description',
                                                      platform=self.stream,
                                                      active=True)
        
    def test_review_create(self):
        data = {
            'author': self.user,
            'rating': 5,
            'description': 'test_descr',
            'watchlist': self.movie,
            'active': True
        }
        
        response = self.client.post(reverse('review-create', args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_review_user(self):
        response = self.client.get('/movie/reviews/?username=' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# class RegisterTestCase(APITestCase):
    
#     def test_register(self):
#         data = {
#             "username": "test_user",
#             "email": "test_email@example.com",
#             "password": "pass123",
#             "password2": "pass123",
#         }
#         response = self.client.post(reverse('register'), data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED) 



# class LoginLogoutTestCase(APITestCase):
    
#     def setUp(self):
#         self.user = User.objects.create_user(username='user', password='password456')
        
#     def test_login(self):
#         data = {
#             "username": "user",
#             "password": "password456",
#             }
#         response = self.client.post(reverse('login'), data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#     def test_logout(self):
#         self.token = Token.objects.get(user__username="user")
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         response = self.client.post(reverse('logout'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


