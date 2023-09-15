from django.urls import reverse
from rest_framework import serializers

from .models import Comment
from ..issue.models import Issue


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Sérialiseur pour le modèle Comment.

    Attributs:
        parent_issue (str): Hyperlien vers l'issue parente du commentaire.
        uuid (str): Hyperlien vers l'API pour la ressource du commentaire.
        author (str): Hyperlien vers l'auteur du commentaire.
    """
    # parent_issue = serializers.HyperlinkedRelatedField(view_name='api:issue-detail', read_only=True)
    # uuid = serializers.HyperlinkedIdentityField(view_name="api:comment-detail", read_only=True)
    author = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True)

    class Meta:
        model = Comment
        fields = ['description', 'author', 'creation_date','uuid']

    def validate(self, attrs):
        """
        Valide et met à jour les attributs du commentaire avec les informations de l'auteur.

        Args:
            attrs (dict): Dictionnaire contenant les attributs du commentaire.

        Returns:
            dict: Dictionnaire mis à jour avec les informations de l'auteur.
        """
        request = self.context.get('request')
        if self.instance is None:

            parsed_url = parse_url(request.get_full_path())
            issue_id = request.data.get('issue_id', parsed_url.get('issue_id', False))
            if not issue_id:
                raise serializers.ValidationError('Please provide a issue_id if not from url')
            attrs['parent_issue'] = Issue.objects.get(pk=issue_id)
            attrs['author'] = request.user

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