from django.urls import path, include
from rest_framework_nested import routers

from .views import ProjectViewSet, IssueViewSet, CommentViewSet
from user.api.api_views import UserViewSet

app_name = 'api'

project_router = routers.DefaultRouter()
project_router.register('project', ProjectViewSet, basename='project')

issue_router = routers.NestedSimpleRouter(project_router, r'project', lookup='project')
issue_router.register(r'issue', viewset=IssueViewSet, basename='issue')
project_router.register('issue', viewset=IssueViewSet, basename='issue')

comment_router = routers.NestedSimpleRouter(issue_router, r'issue', lookup='issue')
comment_router.register(r'comment', viewset=CommentViewSet, basename='comment')
project_router.register('comment', viewset=CommentViewSet, basename='comment')

project_router.register(r'user', viewset=UserViewSet, basename='user')

# routes = project_router.get_routes(ProjectViewSet)
# action_list = []
# for route in routes:
#     action_list += list(route.mapping.values())
# distinct_action_list = set(action_list)
# print(distinct_action_list)

urlpatterns = [
    path('', include(project_router.urls)),
    path('', include(issue_router.urls), name='issue'),
    path('', include(comment_router.urls), name='comment'),
    path('api-auth/', include('rest_framework.urls')),

]


