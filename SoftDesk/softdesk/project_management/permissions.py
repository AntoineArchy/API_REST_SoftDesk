from rest_framework import permissions

class IsContributor(permissions.BasePermission):
    """
    Classe de permission permettant de vérifier si l'utilisateur est un contributeur d'une ressource.
    """
    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l'utilisateur est un contributeur de la ressource.

        Args:
            request: L'objet de requête HTTP.
            view: La vue associée à la requête.
            obj: L'objet de la ressource sur lequel effectuer la vérification.

        Returns:
            bool: True si l'utilisateur est un contributeur, sinon False.
        """
        return request.user in obj.contributors.all()

class IsAuthor(permissions.BasePermission):
    """
    Classe de permission permettant de vérifier si l'utilisateur est l'auteur d'une ressource ou un superutilisateur.
    """
    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l'utilisateur est l'auteur de la ressource ou un superutilisateur.

        Args:
            request: L'objet de requête HTTP.
            view: La vue associée à la requête.
            obj: L'objet de la ressource sur lequel effectuer la vérification.

        Returns:
            bool: True si l'utilisateur est l'auteur ou un superutilisateur, sinon False.
        """
        return obj.author == request.user or request.user.is_superuser
