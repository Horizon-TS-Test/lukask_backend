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
    """
    Este modelo permite gestionar la informacion de personas
    Campos: id_persona, edad, cédula, nombre, apellido, teléfono, direccion,
    fecha_registro, usuario_registro, fecha_actualizacion,  usuario_actualizacion, activo
    """
    id_person = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    age = models.IntegerField()
    identification_card = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=10)
    address = models.CharField(max_length=75)
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField()
    active = models.BooleanField(default=True)
    user_register = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_update = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_update_pr")

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
    """
     Este modelo permite gestionar los perfiles
     Campos: id_perfil, descripcion, fecha_registro, fecha_actualizacion,
      activo, usuario_registro,  usuario_actualizacion
     """
    id_profile= models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    description = models.CharField(max_length=75)
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField()
    active = models.BooleanField(default=True)
    user_register = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_register_pf")
    user_update = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_update_pf")
    users = models.ManyToManyField(
                    UserProfile,
                    through='ProfileUser',
                    through_fields=('profile', 'user'))

# TABLE USER PROFILE n-n
class ProfileUser(models.Model):
    """
     Este modelo permite gestionar los perfiles de los usuarios
     Campos: fecha_login, fecha_registro, fecha_actualizacion
     activo, usuario, perfil, usuario_registro, usuario_actualizacion
    """
    date_login = models.DateTimeField()
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField()
    active = models.BooleanField(default=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user_register = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_register_pu")
    user_update = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null = True, related_name = "user_update_pu")


# TABLE PRIORITY PUBLICATIONS
class PriorityPublication(models.Model):
    """
    Este modelo permite gestionar la prioridad que tiene cada una de las publicaciones de los usuarios
    Campos: id_prioridad_publicacion, descripcion, fecha_registro, fecha_actualizacion, activo
     usuario_registro, usuario_actualizacion
     """
    id_priority_publication = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    description = models.CharField(max_length=75)
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField()
    active = models.BooleanField(default=True)
    user_register = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_update = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null = True, related_name="user_update_pp")



# TABLE TYPE PUBLICATIONS

class TypePublication(models.Model):
    """
    Permite gestionar los tipos de publicaciones
    Campos: id_tipo_publicacion, descripcion, fecha_registro, fecha_actualizacion
    usuario_registro, activo,  usuario_actualizacion
    """
    id_type_publication = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    description = models.CharField(max_length=75)
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField()
    active = models.BooleanField(default=True)
    user_register = models.ForeignKey('userProfile', on_delete=models.CASCADE)
    user_update = models.ForeignKey('userProfile', on_delete=models.CASCADE, null = True, related_name="user_update_tp")


# TABLE TRACING
class Tracing(models.Model):
    """
    Permite gestionar el seguimiento de las publicaciones realizadas por los usuarios
    Campos: id_seguimiento, porcentaje de avance, fecha_inicio, fecha_fin_estimada, fecha_fin_real,
    fecha_registro, fecha_actualizacion, activo, usuario_registro,
    usuario_registro, usuario_actualizacion
    """
    id_tracing = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    percentage_avance = models.FloatField()
    date_start = models.DateTimeField()
    estimated_end_date = models.DateTimeField()
    real_end_date = models.DateTimeField()
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField()
    active = models.BooleanField(default=True)

    user_register = models.ForeignKey('userProfile', on_delete=models.CASCADE)
    user_update = models.ForeignKey('userProfile', on_delete=models.CASCADE, null = True, related_name="user_update_tc")



# TABLE ACTIVITY

class Activity(models.Model):
    """
     Permite gestionar el seguimiento de las publicaciones realizadas por los usuarios
     Campos: id_actividad, descripcion, fecha_inicio_estimada, fecha_fin_real, fecha_fin_estimada, fecha_fin_real,
     fecha_registro, fecha_actualizacion, publicado, activo, seguimiento,
     usuario_registro, usuario_actualizacion
       """
    id_activity = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    description_activity = models.CharField(max_length=75)
    estimated_start_date = models.DateTimeField()
    real_start_date =  models.DateTimeField()
    estimated_end_date = models.DateTimeField()
    real_end_date = models.DateTimeField()
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField()
    published = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    tracing = models.ForeignKey('tracing', on_delete=models.CASCADE) # FK TABLE TRACING
    user_register = models.ForeignKey('userProfile', on_delete=models.CASCADE)
    user_update = models.ForeignKey('userProfile', on_delete=models.CASCADE, null=True, related_name="user_update_at")


# TABLE PUBLICATIONS

class Publication(models.Model):
    """
    Este modelo permite gestionar las publicaciones que realicen los usuarios
    Campos: id_publicacion, latitud, longitud,  detalle, fecha_publicacion,
    fecha_registro, fecha_actualizacion, activo,  prioridad_publicacion, tipo_publicacion, seguimiento,
     usuario_registro, usuario_actualizacion
    """
    id_publication = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    latitude = models.FloatField()
    length = models.FloatField()
    detail = models.TextField(max_length= 300)
    date_publication = models.DateTimeField()
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField()
    active = models.BooleanField(default=True)
    priority_publication = models.ForeignKey('priorityPublication', on_delete=models.CASCADE) # FK TABLE PRIORITY_PUBLICATION
    type_publication = models.ForeignKey('typePublication', on_delete=models.CASCADE) # FK TABLE TYPE_PUBLICATION
    activity = models.ForeignKey('activity', on_delete=models.CASCADE)  # FK TABLE ACTIVITY
    tracing = models.ForeignKey('tracing', on_delete=models.CASCADE)  # FK TABLE ACTIVITY
    user_register = models.ForeignKey('userProfile', on_delete=models.CASCADE,  null=True)
    user_update = models.ForeignKey('userProfile', on_delete=models.CASCADE, null=True, related_name="user_update_pl")

# TABLA DE TIPO DE ACCION
class TypeAccion(models.Model):
    """
    Permite la administracion de tipos de acciones que se realizara sobre una determinada
    notificacion.
    """
    id_tipo_accion      =   models.UUIDField(primary_key= True, default=uuid.uuid4(), editable= False)
    description_acction =   models.CharField(max_length=75)
    date_register       =   models.DateTimeField(auto_created=True)
    date_update         =   models.DateTimeField()
    active              =   models.BooleanField(default=True)
    user_register       =   models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    user_update         =   models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_update_ta")


# TABLA SERVICIOS BASICOS
class ActionNotification(models.Model):
    """
    Permite gestionar las acciones que se realizan sobre una notificacion, Ejemplo:
    Me intersa, Compartir, etiquetar, recomendat, etc.
    """
    id_action_notification  =   models.UUIDField(primary_key = True, default=uuid.uuid4(), editable = False)
    date_register           =   models.DateTimeField(auto_created=True)
    date_update             =   models.DateTimeField()
    active                  =   models.BooleanField(default=True)
    user_register           =   models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    user_update             =   models.ForeignKey(UserProfile, on_delete = models.CASCADE, null=True, related_name = "user_update_an")
    tipo_accion             =   models.ForeignKey(TypeAccion, on_delete= models.CASCADE)


# TABLA MULTIMEDIA
class Multimedia(models.Model):
    """
    Se encarga de almacenar los archivos multimeria de publicacion.
    """
    audio = 'AD'
    video = 'VD'
    image = 'IG'
    file  = 'FL'
    format_multimedia_choices = (
        (audio, 'AUDIO'),
        (video, 'VIDEO'),
        (image, 'IMAGE'),
        (file, 'FILE')
    )
    format_multimedia   =   models.CharField(max_length=2, choices= format_multimedia_choices, default = image)
    id_multimedia       =   models.UUIDField(primary_key=True, default=uuid.uuid4(), editable = False)
    name_file           =   models.CharField(max_length=50)
    description_file    =   models.CharField(max_length=50)
    path_file           =   models.TextField(max_length=200)
    date_register       =   models.DateTimeField(auto_created=True)
    date_update         =   models.DateTimeField()
    active              =   models.BooleanField(default=True)
    user_register       =   models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    user_update         =   models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_update_mul")
