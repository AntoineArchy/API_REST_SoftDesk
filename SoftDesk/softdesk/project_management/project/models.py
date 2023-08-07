import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as lazy_text

from user.models import User


# Create your models here.
class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACK_END = 'BCK', lazy_text("Back-end")
        FRONT_END = 'FRT', lazy_text("Front-end")
        IOS = 'IOS', lazy_text("iOS")
        ANDROID = 'ADR', lazy_text("Android")
        # UNDEFINED = 'UND', lazy_text("Undefined")

    author = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               related_name='project_author',
                               blank=True,
                               null=True)

    description = models.TextField(max_length=800)

    name = models.CharField(max_length=128)
    type = models.CharField(
        max_length=3,
        choices=ProjectType.choices,
        blank=True,
        null=True
    )
    contributors = models.ManyToManyField(to=User,
                                          related_name='project_contributor',
                                          blank=True)

    creation_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
