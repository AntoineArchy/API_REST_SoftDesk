from django.urls import reverse
from rest_framework import serializers

from user.models import User
from .models import Project


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:project-detail")
    author = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True)
    contributors = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True, many=True)
    # issue = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['url', 'author', 'description', 'contributors', 'name']


    # def get_issue(self, obj):
    #     request = self.context.get('request')
    #     return request.build_absolute_uri(reverse('api:puser-detail',
    #                                               kwargs={'user__pk': obj.id}))

    def create(self, validated_data):
        """
            create a new project with request_user as author
            and add a contributor link with role author
            between the project and the request_user
        """
        try:

            request_user = self.context.get('request').user


            validated_data["author"] = request_user
            project = Project.objects.create(**validated_data)
            project.contributors.add(request_user)
            project.save()

            return project

        except KeyError:
            raise serializers.ValidationError('Error in creating project')
