from rest_framework import serializers

from .models import Issue
from project_management.project.serializer import ProjectSerializer
from ..project.models import Project


class IssuSerializer(serializers.HyperlinkedModelSerializer):
    project = serializers.HyperlinkedIdentityField(view_name='api:project-detail')
    author = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="api:issue-detail")

    class Meta:
        model = Issue
        fields = ['url', 'author', 'description', 'name', 'project',
                  'priority', 'tag', 'statut']
    def create(self, validated_data):
        """
            create a new project with request_user as author
            and add a contributor link with role author
            between the project and the request_user
        """
        try:
            request = self.context.get('request')
            url = request.get_full_path()
            url_split = url.split('/')
            print(url, url_split)
            print([(index, elt) for elt, index in enumerate(url_split)])
            validated_data['project'] = Project.objects.get(pk=int(url_split[3]))
            issue = Issue.objects.create(**validated_data)

            request_user = self.context.get('request').user
            issue.author = request_user
            issue.save()

            return issue

        except KeyError:
            raise serializers.ValidationError('Error in creating project')