from django.urls import path

from django.urls import include
from rest_framework import routers

from user.api import api_views

routers = routers.DefaultRouter()
routers.register(r'users', api_views.UserViewSet)

urlpatterns = [
    path('users', include(routers.urls)),
    ]