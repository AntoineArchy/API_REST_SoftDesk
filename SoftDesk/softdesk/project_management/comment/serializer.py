from django.urls import reverse
from rest_framework import serializers

from .models import Comment
from ..issue.models import Issue


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    parent_issue = serializers.HyperlinkedRelatedField(view_name='api:issue-detail', read_only=True)
    uuid = serializers.HyperlinkedIdentityField(view_name="api:comment-detail", read_only=True)
    author = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True)

    class Meta:
        model = Comment
        fields = ['parent_issue', 'uuid', 'author', 'description', ]

    def validate(self, attrs):
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
    parsed_url = dict()
    split_url = url.split('/')
    for url_idx, url_part in enumerate(split_url):
        if not url_part.isdigit():
            continue
        parsed_url[f"{split_url[url_idx - 1]}_id"] = url_part
    return parsed_url