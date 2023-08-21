from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ProjectViewSet, IssueViewSet, CommentViewSet
from user.api.api_views import UserViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
# urlpatterns = [
#     # YOUR PATTERNS
#
#     # Optional UI:
#     path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
# ]
app_name = 'api'

project_router = routers.DefaultRouter()
project_router.register('project', ProjectViewSet, basename='project')

project_router.register('issue', viewset=IssueViewSet, basename='issue')
project_router.register('comment', viewset=CommentViewSet, basename='comment')
project_router.register(r'user', viewset=UserViewSet, basename='user')


issue_router = routers.NestedSimpleRouter(project_router, r'project', lookup='project')
issue_router.register(r'issue', viewset=IssueViewSet, basename='issue')

comment_router = routers.NestedSimpleRouter(issue_router, r'issue', lookup='issue')
comment_router.register(r'comment', viewset=CommentViewSet, basename='comment')


# routes = project_router.get_routes(ProjectViewSet)
# print(routes)
# action_list = []
# for route in routes:
#     action_list += list(route.mapping.values())
#     print(route.mapping)
# distinct_action_list = set(action_list)
# print(distinct_action_list)

urlpatterns = [
    path('', include(project_router.urls)),
    path('', include(issue_router.urls), name='issue'),
    path('', include(comment_router.urls), name='comment'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),

    path(r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]


