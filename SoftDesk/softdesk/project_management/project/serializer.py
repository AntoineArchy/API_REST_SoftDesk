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
        fields = ['url', 'author', 'description', 'contributors', 'name', 'type']


    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user

        attrs['author'] = user
        attrs['contributors'] = [user]

        return attrs