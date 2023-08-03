import datetime

from django.db import models
from django.utils import timezone

from user.models import User


# Create your models here.
class Project(models.Model):
    author = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               related_name='Author')
    description = models.TextField(max_length=800)

    name = models.CharField(max_length=128)
    type = ''
    contributors = models.ManyToManyField(to=User,
                                          related_name='Contributor')

    creation_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
