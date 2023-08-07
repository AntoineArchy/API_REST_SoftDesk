from rest_framework import serializers

from .models import Issue
from project_management.project.serializer import ProjectSerializer
from ..project.models import Project


class IssuSerializer(serializers.HyperlinkedModelSerializer):
    parent_project = serializers.HyperlinkedRelatedField(view_name='api:project-detail', read_only=True)
    author = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="api:issue-detail")

    class Meta:
        model = Issue
        fields = ['url', 'author', 'description', 'name', 'parent_project',
                  'priority', 'tag', 'statut']

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        project_id = request.data.get('project_id', False)
        instance = getattr(self, 'instance', None)

        if instance is not None:
            project_id = instance.parent_project.pk

        if not project_id:
            url = request.get_full_path()
            url_split = url.split('/')
            if url_split[2] != 'project':
                raise serializers.ValidationError('If you\'r not creating from full url, please provide project_id')
            project_id = url_split[3]
        attrs['parent_project'] = Project.objects.get(pk=project_id)
        attrs['author'] = user

        return attrs