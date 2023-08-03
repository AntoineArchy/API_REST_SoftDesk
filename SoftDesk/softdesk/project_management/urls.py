from django.urls import path, include

from project_management.api.v1 import urls as api_urls

urlpatterns = [
    path('api/', include(api_urls)),
]