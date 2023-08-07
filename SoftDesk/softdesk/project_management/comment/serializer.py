from django.urls import reverse
from rest_framework import serializers

from .models import Comment
from ..issue.models import Issue


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    parent_issue = serializers.HyperlinkedRelatedField(view_name='api:issue-detail', read_only=True)
    author = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="api:comment-detail")

    class Meta:
        model = Comment
        fields = ['url', 'author', 'description', 'parent_issue']
        extra_kwargs = {}

    def get_issue(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri()

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        issue_id = request.data.get('issue_id', False)
        instance = getattr(self, 'instance', None)

        if instance is not None:
            issue_id = instance.parent_issue.pk

        if not issue_id:
            url = request.get_full_path()
            url_split = url.split('/')
            if url_split[4] != 'issue':
                raise serializers.ValidationError('If you\'r not creating from full url, please provide issue_id')
            issue_id = url_split[5]
        attrs['parent_issue'] = Issue.objects.get(pk=issue_id)
        attrs['author'] = user
        return attrs