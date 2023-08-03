from rest_framework import viewsets, permissions

from user.models import User
from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint permettant aux utilisateurs d'être vu ou modifié
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]