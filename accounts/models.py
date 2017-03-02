from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in


def update_last_login(sender, user, **kwargs):
    """
    A signal reciever which updates the last_login date for the user logging in.
    """
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])

user_logged_in.connect(update_last_login)


class AccountUserManager(UserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=email, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):
    # now that we've abstracted this class we can add any
    # number of custom attributes to our user class
    stripe_id = models.CharField(max_length=40, default='')
    objects = AccountUserManager()

