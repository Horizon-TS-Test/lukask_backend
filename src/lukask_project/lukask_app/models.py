from django.db import models

import uuid
import django

# FOR AUTHENTICATION:
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
# PERMISSIONS FOR SPECIFIC USERS TO LET THEM TO DO SOMETHING:
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

# MANAGER CLASS TO HANDLE ALL MODELS:


class UserProfileManager(BaseUserManager):
    """
    HELPS DJANGO WORK WITH OUR CUSTOM USER MODEL.
    """

    def create_user(self, email, ci_ruc, first_name, last_name, password):
        """
        CREATES A NEW USER PROFILE OBJECTS
        """

        if not email:
            raise ValueError('Users must have an email address.')

        # CONVERTS EVERY EMAIL CHARACTER TO LOWERCASE:
        # REF: https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager.normalize_email
        email = self.normalize_email(email)
        #

        user = self.model(email=email, ci_ruc=ci_ruc, first_name=first_name, last_name=last_name)

        # NEXT FUNCTIONS WILL ENCRYPT PASSWORD FOR US, RETURNING A HASH TO BE
        # STORED IN OUR DATABASE:
        user.set_password(password)
        #
        user.save(using=self._db)

        return user

    def create_superuser(self, email, ci_ruc, first_name, last_name, password):
        """
        CREATES AND SAVES A NEW SUPERUSER WITH GIVEN DETAILS:
        """

        user = self.create_user(email, ci_ruc, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    REPRESENT A "USER PROFILE" INSIDE OUR APP.
    """

    # DJANGO MODELS REF: https://docs.djangoproject.com/en/1.11/topics/db/models/
    email = models.EmailField(max_length=100, unique=True)
    ci_ruc = models.CharField(max_length=13, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=django.utils.timezone.now, blank=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'  # EMAIL IS REQUIRED BY DEFAULT
    REQUIRED_FIELDS = ['ci_ruc', 'first_name', 'last_name']

    def get_full_name(self):
        """
        USED TO GET A USER'S FULL NAME
        """
        return self.first_name + self.last_name

    def get_short_name(self):
        """
        USED TO GET A USER'S SHORT NAME
        """
        return self.first_name

    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return self.email