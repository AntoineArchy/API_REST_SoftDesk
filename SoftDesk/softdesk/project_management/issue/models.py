import datetime

from django.db import models
from django.utils import timezone

from project_management.project.models import Project
from user.models import User
from django.utils.translation import gettext_lazy as lazy_text


# Create your models here.
class Issue(models.Model):
    class IssuePriority(models.TextChoices):
        LOW = 'LOW', lazy_text("Low")
        MEDIUM = 'MED', lazy_text("Medium")
        HIGH = 'HIG', lazy_text("High")

    class IssueType(models.TextChoices):
        BUG = 'BUG', lazy_text("Bug")
        FEATURE = 'FTR', lazy_text("Feature")
        TASK = 'TSK', lazy_text("Task")

    class IssueStatut(models.TextChoices):
        TO_DO = 'TDO', lazy_text("To-Do")
        IN_PROGRESS = 'INP', lazy_text("In Progress")
        FINISHED = 'FIN', lazy_text("Finished")

    author = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               related_name='issue_author'
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
        return self.parent_project.contributors

    def set_assignation(self, assignee):
        self.assignee = assignee
        self.save()
