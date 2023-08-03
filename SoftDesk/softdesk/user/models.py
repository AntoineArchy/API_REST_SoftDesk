from datetime import datetime, timedelta

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import CheckConstraint, Q


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, username, password, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'birthday']

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
