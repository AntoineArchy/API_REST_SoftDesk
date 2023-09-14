from django.urls import reverse
from rest_framework import serializers

from user.models import User
from .models import Project


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    """
    Sérialiseur pour le modèle de projet.

    Attributs:
        url (str): URL de l'API pour la ressource du projet.
        author (str): Hyperlien vers l'auteur du projet.
        contributors (list of str): Hyperliens vers les contributeurs du projet.
    """
    url = serializers.HyperlinkedIdentityField(view_name="api:project-detail")
    author = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True)
    contributors = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True, many=True)

    # issue = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['url', 'name', 'description', 'type', 'author', 'contributors']

    def validate(self, attrs):
        """
        Valide et met à jour les attributs du projet avec l'auteur et les contributeurs.

        Args:
            attrs (dict): Dictionnaire contenant les attributs du projet.

        Returns:
            dict: Dictionnaire mis à jour avec l'auteur et les contributeurs.
        """
        request = self.context.get('request')
        user = request.user

        attrs['author'] = user
        attrs['contributors'] = [user]

        return attrs
