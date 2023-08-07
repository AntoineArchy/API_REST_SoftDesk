import datetime

from django.db import models
from django.utils import timezone

from project_management.project.models import Project
from user.models import User


# Create your models here.
class Issue(models.Model):
    author = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               related_name='issue_author',
                               blank=True,
                               null=True
                               )
    description = models.TextField(max_length=800)

    name = models.CharField(max_length=128)
    parent_project = models.ForeignKey(to=Project,
                                       on_delete=models.CASCADE,
                                       related_name='project')
    priority = ''
    tag = ''
    statut = ''

    creation_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    @property
    def contributors(self):
        return self.parent_project.contributors
