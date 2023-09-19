import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as lazy_text

from user.models import User


# Create your models here.
class Project(models.Model):
    """
        Modèle représentant un projet.

        Attributs:
        author (User): L'auteur du projet.
        description (str): La description du projet (jusqu'à 800 caractères).
        name (str): Le nom du projet (jusqu'à 128 caractères).
        type (str): Le type du projet, choisi parmi les options prédéfinies.
        contributors (list of User): Les utilisateurs qui contribuent au projet.
        creation_date (datetime): La date et l'heure de création du projet.
        """

    class ProjectType(models.TextChoices):
        """
                Choix disponibles pour le type de projet.
                """
        BACK_END = 'BCK', lazy_text("Back-end")
        FRONT_END = 'FRT', lazy_text("Front-end")
        IOS = 'IOS', lazy_text("iOS")
        ANDROID = 'ADR', lazy_text("Android")

    author = models.ForeignKey(to=User,
                               on_delete=models.SET_NULL,
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

    def add_contributors(self, *contributors):
        """
       Ajoute des contributeurs au projet.

       Args:
           *contributors (User): Une ou plusieurs instances User à ajouter en tant que contributeurs.

       Returns:
           None
       """

        for contributor in contributors:
            self.contributors.add(contributor)
        self.save()
