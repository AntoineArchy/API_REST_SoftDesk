from string import digits

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from user.models import User
from .models import Issue
from ..project.models import Project


class IssuSerializer(serializers.HyperlinkedModelSerializer):
    """
    Sérialiseur pour le modèle Issue.

    Attributs:
        parent_project (str): Hyperlien vers le projet parent de l'issue.
        author (str): Hyperlien vers l'auteur de l'issue.
        url (str): URL de l'API pour la ressource de l'issue.
        assignee (str): Hyperlien vers l'utilisateur assigné à l'issue.
    """
    parent_project = serializers.HyperlinkedRelatedField(view_name='api:project-detail', read_only=True)
    author = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="api:issue-detail")
    assignee = serializers.HyperlinkedRelatedField(view_name="api:user-detail", allow_null=True, read_only=True)

    class Meta:
        model = Issue
        fields = ['url', 'author', 'description', 'name', 'parent_project',
                  'priority', 'issue_type', 'statut', 'assignee']

    def validate(self, attrs):
        """
        Valide et met à jour les attributs de l'issue avec les informations de l'auteur et de l'assigné.

        Args:
            attrs (dict): Dictionnaire contenant les attributs de l'issue.

        Returns:
            dict: Dictionnaire mis à jour avec les informations de l'auteur et de l'assigné.
        """
        request = self.context.get('request')
        if self.instance is None:
            parsed_url = parse_url(request.get_full_path())
            project_id = request.data.get('project_id', parsed_url.get('project_id', False))
            if not project_id:
                raise serializers.ValidationError('Please provide a project_id if not from url')
            attrs['parent_project'] = Project.objects.get(pk=project_id)
            attrs['author'] = request.user

        if request.data.get('assignee_id', False):
            try:
                assigned_user = User.objects.get(pk=request.data.get('assignee_id'))
            except ObjectDoesNotExist:
                raise serializers.ValidationError('assignee id does not match a known user')

            if assigned_user not in attrs['parent_project'].contributors.all():
                raise serializers.ValidationError('Assignee id does not match any known contributor')
            attrs['assignee'] = assigned_user
        return attrs


def parse_url(url):
    """
    Analyse une URL pour extraire les identifiants des ressources.

    Args:
        url (str): URL à analyser.

    Returns:
        dict: Dictionnaire contenant les identifiants des ressources.
    """
    parsed_url = dict()
    split_url = url.split('/')
    for url_idx, url_part in enumerate(split_url):
        if not url_part.isdigit():
            continue
        parsed_url[f"{split_url[url_idx - 1]}_id"] = url_part
    return parsed_url
