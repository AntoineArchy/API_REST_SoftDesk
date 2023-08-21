from string import digits

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from user.models import User
from .models import Issue
from ..project.models import Project


class IssuSerializer(serializers.HyperlinkedModelSerializer):
    parent_project = serializers.HyperlinkedRelatedField(view_name='api:project-detail', read_only=True)
    author = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="api:issue-detail")
    assignee = serializers.HyperlinkedRelatedField(view_name="api:user-detail", allow_null=True, read_only=True)

    class Meta:
        model = Issue
        fields = ['url', 'author', 'description', 'name', 'parent_project',
                  'priority', 'issue_type', 'statut', 'assignee']

    def validate(self, attrs):
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
    parsed_url = dict()
    split_url = url.split('/')
    for url_idx, url_part in enumerate(split_url):
        if not url_part.isdigit():
            continue
        parsed_url[f"{split_url[url_idx - 1]}_id"] = url_part
    return parsed_url
