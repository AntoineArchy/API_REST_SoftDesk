from rest_framework import viewsets, permissions

from user.models import User
from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    VueSet pour le modèle User.

    Attributs:
        queryset (QuerySet): Ensemble des objets User à utiliser.
        serializer_class: Classe de sérialiseur à utiliser pour le modèle User.
        permission_classes (list of classes): Classes de permission pour restreindre l'accès à la vue.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]