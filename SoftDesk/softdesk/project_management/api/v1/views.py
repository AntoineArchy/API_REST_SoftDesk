from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

import project_management.permissions as pm_permissions

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

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_admin:
            return project_models.Project.objects.all().order_by('creation_date')
        return project_models.Project.objects.filter(contributors=user)

    def get_permissions(self):
        # print(self.kwargs)
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsContributor]
        return [permission() for permission in permission_classes]


class IssueViewSet(viewsets.ModelViewSet):
    queryset = issue_models.Issue.objects.all()
    serializer_class = issue_serializers.IssuSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        project_pk = self.kwargs.get('project_pk', False)

        if project_pk:
            return issue_models.Issue.objects.filter(parent_project__pk=project_pk).order_by('last_update')

        if user.is_superuser or user.is_admin:
            return issue_models.Issue.objects.all().order_by('creation_date')

        return issue_models.Issue.objects.filter(
            parent_project__pk__in=project_models.Project.objects.filter(
                contributors=user).values('pk')
        ).order_by("parent_project_id", 'last_update')

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsContributor]
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = comment_models.Comment.objects.all()
    serializer_class = comment_serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        issue_pk = self.kwargs.get('issue_pk', False)

        if issue_pk:
            return comment_models.Comment.objects.filter(parent_issue__pk=issue_pk)

        if user.is_superuser or user.is_admin:
            return comment_models.Comment.objects.all().order_by('creation_date')

        return comment_models.Comment.objects.filter(parent_issue__in=issue_models.Issue.objects.filter(
            parent_project__contributors=user))

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsContributor]
        return [permission() for permission in permission_classes]
