import datetime

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

    issue = models.ForeignKey(to=Issue,
                              on_delete=models.CASCADE)
    uuid = ''

    creation_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
