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
from pip.cmdoptions import editable


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

#--------------------------------------------------------------------------------------#
#---------------DEFINICION DE MODELOS DE BASE DE DATOS PARA APLICACION LUKASK----------#
#--------------------------------------------------------------------------------------#

    # TABLE PERSON
class Person(models.Model):
    id_person = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    identification_card = models.TextField(max_length=13)
    name = models.TextField(max_length=50)
    last_name = models.TextField(max_length=50)
    age = models.IntegerField()
    telephone = models.TextField(max_length=10)
    address = models.TextField(max_length=75)
    date_register = models.DateTimeField(auto_now_add=True)
    user_register = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_update = models.DateTimeField()
    user_update = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def get_full_name(self):
        """
        USED TO GET A USER'S FULL NAME
        """
        return self.name + self.last_name

    def get_short_name(self):
        """
        USED TO GET A USER'S SHORT NAME
        """
        return self.name



 # TABLE PROFILE

class Profile(models.Model):
    id_profile= models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    description = models.TextField(max_length=100)
    users = models.ManyToManyField(
                    UserProfile,
                    through='ProfileUser',
                    through_fields=('profile', 'user'))
    date_register = models.DateTimeField(auto_now_add=True)
    user_register = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_update = models.DateTimeField()
    user_update = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)




# TABLE USER PROFILE n-n

class ProfileUser(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_login = models.DateTimeField()
    date_register = models.DateTimeField(auto_now_add=True)
    user_register = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_update = models.DateTimeField()
    user_update = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)


# TABLE PUBLICATIONS

class Publication(models.Model):
    id_publication = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    detail = models.TextField(max_length= 300)
    date_publication = models.DateTimeField()
    latitude = models.FloatField()
    length = models.FloatField()
    priority_publication = models.ForeignKey(PriorityPublication, on_delete=models.CASCADE) # FK TABLE PRIORITY_PUBLICATION
    type_publication = models.ForeignKey(TypePublication, on_delete=models.CASCADE) # FK TABLE TYPE_PUBLICATION



# TABLE PRIORITY PUBLICATIONS

class PriorityPublication:
    id_priority_publication = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    description = models.TextField(max_length=100)


# TABLE TYPE PUBLICATIONS

class TypePublication:
    id_type_publication = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    description = models.TextField(max_length=100)



# TABLE ACTIVITY


# TABLA SERVICIOS BASICOS

class ActionNotification(models.Model):
    """
    Permite gestionar las acciones que se realizan sobre una notificacion, Ejemplo:
    Me intersa, Compartir, etiquetar, recomendat, etc.
    """
    id_action_notication = models.UUIDField(primary_key = True, default=uuid.uuid4(), editable = False)
    date_register = models.DateTimeField(auto_created=True)
    user_register = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
    date_update = models.DateTimeField()
    user_update = models.ForeignKey(UserProfile, on_delete = models.CASCADE(null=True))
    active = models.BooleanField(default=True)
    tipo_accion = models.ForeignKey(TipoAccion, on_delete= models.CASCADE(null=True))


# TABLA DE TIPO DE ACCION
class TipoAccion(models.Model):
    """
    Permite la administracion de tipos de acciones que se realizara sobre una determinada
    notificacion.
    """
    id_tipo_accion = models.UUIDField(primary_key= True, default=uuid.uuid4(), editable= False)
    description_acction = models.TextField();
    date_register = models.DateTimeField(auto_created=True)
    user_register = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    date_update = models.DateTimeField()
    user_update = models.ForeignKey(UserProfile, on_delete=models.CASCADE(null=True))
    active = models.BooleanField(default=True)

