from datetime import datetime, timedelta

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import CheckConstraint, Q


class UserManager(BaseUserManager):
    """
    Manager pour les profils d'utilisateurs.

    Méthodes:
        create_user: Crée un utilisateur.
        create_superuser: Crée un superutilisateur.
    """
    def create_user(self, username, password, **kwargs):
        """
        Crée un nouvel utilisateur.

        Args:
            username (str): Nom d'utilisateur.
            password (str): Mot de passe.

        Returns:
            User: Instance de l'utilisateur créé.
        """
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **kwargs):
        """
        Crée un superutilisateur.

        Args:
            username (str): Nom d'utilisateur.
            password (str): Mot de passe.

        Returns:
            User: Instance du superutilisateur créé.
        """
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modèle représentant un utilisateur.

    Attributs:
        username (str): Nom d'utilisateur (unique).
        birthday (datetime): Date de naissance.
        date_joined (datetime): Date d'adhésion.
        can_be_contacted (bool): Peut être contacté.
        can_data_be_shared (bool): Les données peuvent être partagées.
        is_admin (bool): Est un administrateur.
        is_active (bool): Est actif.
        is_staff (bool): Est membre du staff.
        is_superuser (bool): Est un superutilisateur.
    """
    username = models.CharField(max_length=255, unique=True)
    birthday = models.DateTimeField(
        blank=False, null=False
    )

    date_joined = models.DateTimeField(
        blank=False, null=False, default=datetime(1970, 1, 1)
    )

    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    objects = UserManager()

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['birthday']

    class Meta:
        constraints = [
            # Ensures constraint on DB level, raises IntegrityError
            CheckConstraint(
                check=
                Q(birthday__lte=(
                        datetime.today() - timedelta(days=365 * 15)
                )),
                name='check_birthday',
            ),
        ]

    def __str__(self):
        return self.username
