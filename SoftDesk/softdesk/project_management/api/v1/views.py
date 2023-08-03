from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
import project_management.project.models as project_models
import project_management.project.serializer as project_serializers

import project_management.comment.models as comment_models
import project_management.comment.serializer as comment_serializers

import project_management.issue.models as issue_models
import project_management.issue.serializer as issue_serializers



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = project_models.Project.objects.all()
    serializer_class = project_serializers.ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class IssueViewSet(viewsets.ModelViewSet):
    queryset = issue_models.Issue.objects.all()
    serializer_class = issue_serializers.IssuSerializer
    permission_classes = [permissions.IsAuthenticated, ]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = comment_models.Comment.objects.all()
    serializer_class = comment_serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticated, ]