from string import digits

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from user.models import User
from .models import Issue
from ..project.models import Project
from ..utils import parse_url


class IssuSerializer(serializers.HyperlinkedModelSerializer):
    """
    Sérialiseur pour le modèle Issue.

    Attributs:
        parent_project (str): Hyperlien vers le projet parent de l'issue.
        author (str): Hyperlien vers l'auteur de l'issue.
        url (str): URL de l'API pour la ressource de l'issue.
        assignee (str): Hyperlien vers l'utilisateur assigné à l'issue.
    """
    author = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True)
    assignee = serializers.HyperlinkedRelatedField(view_name="api:user-detail", allow_null=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="api:issue-detail", read_only=True)

    class Meta:
        model = Issue
        fields = ['name', 'description', 'priority', 'issue_type', 'statut', 'assignee', 'author', 'id', 'url']

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
                raise serializers.ValidationError('assignee id does not match any known user')

            if assigned_user not in attrs.get('parent_project', self.instance.parent_project).contributors.all():
                raise serializers.ValidationError('Assignee id does not match any known contributor')
            attrs['assignee'] = assigned_user
        return attrs