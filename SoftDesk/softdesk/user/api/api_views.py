from rest_framework import viewsets, permissions
from rest_framework.response import Response

from project_management.project.models import Project
from user.models import User
from user.serializers import UserSerializer

import project_management.permissions as pm_permissions


class UserViewSet(viewsets.ModelViewSet):
    """
    VueSet pour le modèle User.

    Attributs:
        queryset (QuerySet): Ensemble des objets User à utiliser.
        serializer_class: Classe de sérialiseur à utiliser pour le modèle User.
        permission_classes (list of classes): Classes de permission pour restreindre l'accès à la vue.
    """

    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [pm_permissions.IsConcernedUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        contribution_to_remove = Project.objects.filter(contributors=user)
        for project in contribution_to_remove:
            project.contributors.remove(user)
        return Response(data='User has been deactivated.')
