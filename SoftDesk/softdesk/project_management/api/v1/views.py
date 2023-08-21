from django.shortcuts import render

from rest_framework import viewsets, permissions, status
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
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsContributor]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk):
        project = project_models.Project.objects.get(pk=pk)
        if request.user in project.contributors.all():
            return Response(status=status.HTTP_208_ALREADY_REPORTED)
        project.add_contributors(request.user)
        project.save()
        return Response(status=status.HTTP_202_ACCEPTED)


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
            parent_project__contributors=user
        ).order_by("parent_project_id", 'last_update')

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsContributor]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['patch'], permission_classes=[pm_permissions.IsContributor])
    def update_issue_info(self, request, *args, **kwargs):
        issue = self.get_object()
        data = request.data
        serializer = issue_serializers.IssuSerializer(issue, context={'request': request}, data=data, partial=True)
        if serializer.is_valid():
            issue.priority = serializer.validated_data.get('priority', issue.priority)
            issue.issue_type = serializer.validated_data.get('issue_type', issue.issue_type)
            issue.statut = serializer.validated_data.get('statut', issue.statut)
            issue.assignee = serializer.validated_data.get('assignee', issue.assignee)

            issue.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
