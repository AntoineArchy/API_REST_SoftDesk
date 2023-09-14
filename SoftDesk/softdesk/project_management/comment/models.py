import datetime

import uuid
from django.db import models
from django.utils import timezone

from ..issue.models import Issue
from user.models import User


# Create your models here.
class Comment(models.Model):
    """
    Modèle représentant un commentaire pour une issue.

    Attributs:
        author (User): L'auteur du commentaire.
        description (str): La description du commentaire (jusqu'à 800 caractères).
        parent_issue (Issue): L'issue parente du commentaire.
        uuid (UUID): Clé primaire unique du commentaire.
        creation_date (datetime): La date et l'heure de création du commentaire.
        last_update (datetime): La date et l'heure de la dernière mise à jour du commentaire.
    """
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
        """
        Renvoie les contributeurs de l'issue parente du commentaire.

        Returns:
            list of User: Liste des contributeurs de l'issue parente.
        """
        return self.parent_issue.contributors