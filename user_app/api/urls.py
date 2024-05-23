from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from user_app.api import views

urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path("register/", views.create_user, name="register"),
]