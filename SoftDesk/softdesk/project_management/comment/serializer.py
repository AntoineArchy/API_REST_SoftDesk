from django.urls import reverse
from rest_framework import serializers

from .models import Comment
from ..issue.models import Issue


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    # issue = serializers.HyperlinkedIdentityField(view_name='api:issue')
    author = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True)
    # url = serializers.HyperlinkedIdentityField(view_name="api:comment-detail")
    issue = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'description', 'issue']
        extra_kwargs = {}

    def get_issue(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri() + 'issue'

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
            # validated_data['project'] = Project.objects.get(pk=int(url_split[3]))
            validated_data['issue'] = Issue.objects.get(pk=int(url_split[5]))

            comment = Comment.objects.create(**validated_data)

            request_user = self.context.get('request').user
            comment.author = request_user
            comment.save()

            return comment

        except KeyError:
            raise serializers.ValidationError('Error in creating project')