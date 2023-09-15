import datetime

from django.db import models
from django.utils import timezone

from project_management.project.models import Project
from user.models import User
from django.utils.translation import gettext_lazy as lazy_text


# Create your models here.
class Issue(models.Model):
    """
    Modèle représentant un problème (issue) dans un projet.

    Attributs:
        author (User): L'auteur de l'issue.
        description (str): La description de l'issue (jusqu'à 800 caractères).
        name (str): Le nom de l'issue (jusqu'à 128 caractères).
        parent_project (Project): Le projet parent de l'issue.
        priority (str): La priorité de l'issue, choisie parmi les options prédéfinies.
        issue_type (str): Le type d'issue, choisi parmi les options prédéfinies.
        statut (str): Le statut actuel de l'issue, choisi parmi les options prédéfinies.
        assignee (User): L'utilisateur assigné à l'issue.
        creation_date (datetime): La date et l'heure de création de l'issue.
        last_update (datetime): La date et l'heure de la dernière mise à jour de l'issue.
    """
    class IssuePriority(models.TextChoices):
        """
        Choix disponibles pour la priorité de l'issue.
        """
        LOW = 'LOW', lazy_text("Low")
        MEDIUM = 'MED', lazy_text("Medium")
        HIGH = 'HIG', lazy_text("High")

    class IssueType(models.TextChoices):
        """
        Choix disponibles pour le type d'issue.
        """
        BUG = 'BUG', lazy_text("Bug")
        FEATURE = 'FTR', lazy_text("Feature")
        TASK = 'TSK', lazy_text("Task")

    class IssueStatut(models.TextChoices):
        """
        Choix disponibles pour le statut de l'issue.
        """
        TO_DO = 'TDO', lazy_text("To-Do")
        IN_PROGRESS = 'INP', lazy_text("In Progress")
        FINISHED = 'FIN', lazy_text("Finished")

    author = models.ForeignKey(to=User,
                               on_delete=models.SET_NULL,
                               related_name='issue_author',
                               null=True,

                               )
    description = models.TextField(max_length=800)

    name = models.CharField(max_length=128)
    parent_project = models.ForeignKey(to=Project,
                                       on_delete=models.CASCADE,
                                       related_name='project')
    priority = models.CharField(
        max_length=3,
        choices=IssuePriority.choices,
        blank=True,
        null=True,
    )
    issue_type = models.CharField(
        max_length=3,
        choices=IssueType.choices,
        blank=True,
        null=True,
    )
    statut = models.CharField(
        max_length=3,
        choices=IssueStatut.choices,
        default=IssueStatut.TO_DO
    )

    assignee = models.ForeignKey(to=User,
                                 on_delete=models.SET_NULL,
                                 related_name='assignee',
                                 null=True,
                                 blank=True)

    creation_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    @property
    def contributors(self):
        """
        Renvoie les contributeurs du projet parent de l'issue.

        Returns:
            list of User: Liste des contributeurs du projet parent.
        """
        return self.parent_project.contributors

    def set_assignation(self, assignee):
        """
        Assigne l'issue à un utilisateur.

        Args:
            assignee (User): L'utilisateur à qui l'issue doit être assignée.

        Returns:
            None
        """
        self.assignee = assignee
        self.save()
