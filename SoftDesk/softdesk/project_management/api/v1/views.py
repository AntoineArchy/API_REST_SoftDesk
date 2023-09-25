from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

import project_management.comment.models as comment_models
import project_management.comment.serializer as comment_serializers
import project_management.issue.models as issue_models
import project_management.issue.serializer as issue_serializers
import project_management.permissions as pm_permissions
import project_management.project.models as project_models
import project_management.project.serializer as project_serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """
    VueSet pour le modèle de projet.

    Attributs:
        queryset (QuerySet): Ensemble des objets Project à utiliser.
        serializer_class: Classe de sérialiseur à utiliser pour le modèle Project.
        permission_classes (list of classes): Classes de permission pour restreindre l'accès à la vue.
    """
    queryset = project_models.Project.objects.all()
    serializer_class = project_serializers.ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        """
        Récupère et renvoie l'ensemble des objets Project selon les permissions de l'utilisateur.

        Returns:
            QuerySet: Ensemble des objets Project.
        """
        user = self.request.user
        if user.is_superuser or user.is_admin:
            return project_models.Project.objects.all().order_by('creation_date')
        return project_models.Project.objects.filter(contributors=user).order_by('creation_date')

    def get_permissions(self):
        """
        Récupère et renvoie les classes de permission en fonction de l'action de la vue.

        Returns:
            list of classes: Classes de permission à appliquer.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsContributor]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk):
        """
        Inscrit l'utilisateur actuel en tant que contributeur au projet spécifié.

        Args:
            request: L'objet de requête HTTP.
            pk (int): Clé primaire du projet auquel l'utilisateur souhaite s'abonner.

        Returns:
            Response: Réponse HTTP indiquant le statut de l'inscription.
        """
        project = project_models.Project.objects.get(pk=pk)
        if request.user in project.contributors.all():
            return Response(status=status.HTTP_208_ALREADY_REPORTED)
        project.add_contributors(request.user)
        project.save()
        return Response(status=status.HTTP_202_ACCEPTED)


@extend_schema(parameters=[OpenApiParameter("project_id", int, OpenApiParameter.PATH, required=False,
                                            description='A unique integer value identifying the parent project.')]
               )
class IssueViewSet(viewsets.ModelViewSet):
    """
    VueSet pour le modèle Issue.

    Attributs:
        queryset (QuerySet): Ensemble des objets Issue à utiliser.
        serializer_class: Classe de sérialiseur à utiliser pour le modèle Issue.
        permission_classes (list of classes): Classes de permission pour restreindre l'accès à la vue.
    """
    queryset = issue_models.Issue.objects.all()
    serializer_class = issue_serializers.IssuSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        """
        Récupère et renvoie l'ensemble des objets Issue en fonction des permissions de l'utilisateur.

        Returns:
            QuerySet: Ensemble des objets Issue.
        """
        user = self.request.user
        project_pk = self.kwargs.get('project_pk', False)

        if project_pk:
            return issue_models.Issue.objects.filter(parent_project__pk=project_pk).order_by('-creation_date')

        if user.is_superuser or user.is_admin:
            return issue_models.Issue.objects.all().order_by('-creation_date')

        return issue_models.Issue.objects.filter(
            parent_project__assignee=user
        ).order_by("parent_project_id", '-creation_date')

    def get_permissions(self):
        """
        Récupère et renvoie les classes de permission en fonction de l'action de la vue.

        Returns:
            list of classes: Classes de permission à appliquer.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsContributor]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['patch'], permission_classes=[pm_permissions.IsContributor])
    def update_issue_info(self, request, *args, **kwargs):
        """
       Met à jour les informations de l'issue spécifiée.

       Args:
           request: L'objet de requête HTTP.
           *args: Arguments positionnels.
           **kwargs: Arguments nommés.

       Returns:
           Response: Réponse HTTP indiquant le statut de la mise à jour.
       """
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


@extend_schema(parameters=[OpenApiParameter("project_id", int, OpenApiParameter.PATH,
                                            description='A unique integer value identifying the parent project.',
                                            required=False),
                           OpenApiParameter("issue_id", int, OpenApiParameter.PATH,
                                            description='A unique integer value identifying the parent issue.')])
class CommentViewSet(viewsets.ModelViewSet):
    """
    VueSet pour le modèle Comment.

    Attributs:
        queryset (QuerySet): Ensemble des objets Comment à utiliser.
        serializer_class: Classe de sérialiseur à utiliser pour le modèle Comment.
        permission_classes (list of classes): Classes de permission pour restreindre l'accès à la vue.
    """
    queryset = comment_models.Comment.objects.all()
    serializer_class = comment_serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        """
        Récupère et renvoie l'ensemble des objets Comment en fonction des permissions de l'utilisateur.

        Returns:
            QuerySet: Ensemble des objets Comment.
        """
        user = self.request.user
        issue_pk = self.kwargs.get('issue_pk', False)

        if issue_pk:
            return comment_models.Comment.objects.filter(parent_issue__pk=issue_pk).order_by('-creation_date')

        if user.is_superuser or user.is_admin:
            return comment_models.Comment.objects.all().order_by('-creation_date')

        return comment_models.Comment.objects.filter(parent_issue__in=issue_models.Issue.objects.filter(
            parent_project__contributors=user)).order_by('-creation_date')

    def get_permissions(self):
        """
        Récupère et renvoie les classes de permission en fonction de l'action de la vue.

        Returns:
            list of classes: Classes de permission à appliquer.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated, pm_permissions.IsContributor]
        return [permission() for permission in permission_classes]
