from django.urls import path

from django.urls import include
from rest_framework import routers

from user.api import api_views
#
# routers = routers.DefaultRouter()
# routers.register(r'user', api_views.UserViewSet, basename='users')
# app_name = 'user'
#
# urlpatterns = [
#     path('user', include(routers.urls)),
#     ]