import datetime

import uuid
from django.db import models
from django.utils import timezone

from ..issue.models import Issue
from user.models import User


# Create your models here.
class Comment(models.Model):
    author = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)
    description = models.TextField(max_length=800)

    parent_issue = models.ForeignKey(to=Issue,
                                     on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    creation_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    @property
    def contributors(self):
        return self.parent_issue.contributors