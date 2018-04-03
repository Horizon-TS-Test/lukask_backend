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






#--------------------------------------------------------------------------------------#
#---------------DEFINICION DE MODELOS DE BASE DE DATOS PARA APLICACION LUKASK----------#
#--------------------------------------------------------------------------------------#

    # TABLE PERSON
class Person(models.Model):
    """
    Este modelo permite gestionar la informacion de personas
    Campos: id_persona, edad, cedula, nombre, apellido, telefono, direccion,
    fecha_registro, usuario_registro, fecha_actualizacion,  usuario_actualizacion, activo
    """
    id_person = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    age = models.IntegerField()
    identification_card = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=10)
    address = models.CharField(max_length=75)
    active = models.BooleanField(default=True)
    #user_register = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #user_update = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_update_pr")

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

    def __str__(self):
        """
        DEVULVE EL IDENTIFICAR O CL DE LA PERSONA
        :return:
        """
        return '%s: %s' % (self.name, self.identification_card)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    REPRESENT A "USER PROFILE" INSIDE OUR APP.
    """

    # DJANGO MODELS REF: https://docs.djangoproject.com/en/1.11/topics/db/models/
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_register = models.DateTimeField(auto_now_add=True)
    person = models.OneToOneField('person', related_name='userProfiles', on_delete=models.CASCADE, null=True)

    #objects = UserProfileManager()

    USERNAME_FIELD = 'email'  # EMAIL IS REQUIRED BY DEFAULT


    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return self.email

 # TABLE PROFILE
class Profile(models.Model):
    """
     Este modelo permite gestionar los perfiles
     Campos: id_perfil, descripcion, fecha_registro, fecha_actualizacion,
      activo, usuario_registro,  usuario_actualizacion
     """
    id_profile= models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    description = models.CharField(max_length=75)
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True, blank=True)
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
    date_update = models.DateTimeField(null=True, blank=True)
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
    id_priority_publication = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    description = models.CharField(max_length=75)
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    user_register = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_update = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null = True, related_name="user_update_pp")


    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return self.description

# TABLE TYPE PUBLICATIONS

class TypePublication(models.Model):
    """
    Permite gestionar los tipos de publicaciones
    Campos: id_tipo_publicacion, descripcion, fecha_registro, fecha_actualizacion
    usuario_registro, activo,  usuario_actualizacion
    """
    id_type_publication = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    description = models.CharField(max_length=75)
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    user_register = models.ForeignKey('userProfile', on_delete=models.CASCADE)
    user_update = models.ForeignKey('userProfile', on_delete=models.CASCADE, null = True, related_name="user_update_tp")


    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return self.description

# TABLE TRACING
class Tracing(models.Model):
    """
    Permite gestionar el seguimiento de las publicaciones realizadas por los usuarios
    Campos: id_seguimiento, porcentaje de avance, fecha_inicio, fecha_fin_estimada, fecha_fin_real,
    fecha_registro, fecha_actualizacion, activo, usuario_registro,
    usuario_registro, usuario_actualizacion
    """
    id_tracing = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    percentage_avance = models.FloatField()
    date_start = models.DateTimeField()
    estimated_end_date = models.DateTimeField()
    real_end_date = models.DateTimeField()
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    publication = models.ForeignKey('publication', on_delete=models.CASCADE, null=True)  # FK TABLE ACTIVITY
    user_register = models.ForeignKey('userProfile', on_delete=models.CASCADE)
    user_update = models.ForeignKey('userProfile', on_delete=models.CASCADE, null = True, related_name="user_update_tc")


    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return '%d %s' % (self.percentage_avance, self.date_start.strftime('%d-%m-%Y'))

# TABLE ACTIVITY

class Activity(models.Model):
    """
     Permite gestionar el seguimiento de las publicaciones realizadas por los usuarios
     Campos: id_actividad, descripcion, fecha_inicio_estimada, fecha_fin_real, fecha_fin_estimada, fecha_fin_real,
     fecha_registro, fecha_actualizacion, publicado, activo, seguimiento,
     usuario_registro, usuario_actualizacion
       """
    id_activity = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    description_activity = models.CharField(max_length=75)
    estimated_start_date = models.DateTimeField()
    real_start_date =  models.DateTimeField()
    estimated_end_date = models.DateTimeField()
    real_end_date = models.DateTimeField()
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True, blank=True)
    published = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    tracing = models.ForeignKey('tracing', on_delete=models.CASCADE) # FK TABLE TRACING
    user_register = models.ForeignKey('userProfile', on_delete=models.CASCADE)
    user_update = models.ForeignKey('userProfile', on_delete=models.CASCADE, null=True, related_name="user_update_at")


    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return self.description_activity

# TABLE PUBLICATIONS

class Publication(models.Model):
    """
    Este modelo permite gestionar las publicaciones que realicen los usuarios
    Campos: id_publicacion, latitud, longitud,  detalle, fecha_publicacion,
    fecha_registro, fecha_actualizacion, activo,  prioridad_publicacion, tipo_publicacion, seguimiento,
     usuario_registro, usuario_actualizacion
    """
    id_publication = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    latitude = models.FloatField()
    length = models.FloatField()
    detail = models.TextField(max_length= 300)
    date_publication = models.DateTimeField()
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    priority_publication = models.ForeignKey('priorityPublication', on_delete=models.CASCADE) # FK TABLE PRIORITY_PUBLICATION
    type_publication = models.ForeignKey('typePublication', on_delete=models.CASCADE) # FK TABLE TYPE_PUBLICATION
    activity = models.ForeignKey('activity', on_delete=models.CASCADE, null=True)  # FK TABLE ACTIVITY

    user_register = models.ForeignKey('userProfile', on_delete=models.CASCADE,  null=True)
    user_update = models.ForeignKey('userProfile', on_delete=models.CASCADE, null=True, related_name="user_update_pl")


    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return '%s %d %d' % (self.detail, self.latitude, self.length)


# TABLA DE TIPO DE ACCION
class TypeAction(models.Model):
    """
    Permite la administracion de tipos de acciones que se realizara sobre una determinada
    notificacion.
    """
    id_type_action = models.UUIDField(primary_key= True, default=uuid.uuid4(), editable= False, unique=True)
    description_action =   models.CharField(max_length=75)
    date_register       =   models.DateTimeField(auto_created=True)
    date_update         =   models.DateTimeField(null=True, blank=True)
    active              =   models.BooleanField(default=True)
    user_register       =   models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    user_update         =   models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_update_ta")


    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return self.description_action

# TABLA SERVICIOS BASICOS
class ActionNotification(models.Model):
    """
    Permite gestionar las acciones que se realizan sobre una notificacion, Ejemplo:
    Me intersa, Compartir, etiquetar, recomendat, etc.
    """
    id_action_notification  =   models.UUIDField(primary_key = True, default=uuid.uuid4(), editable = False, unique=True)
    date_register           =   models.DateTimeField(auto_created=True)
    date_update             =   models.DateTimeField(null=True, blank=True)
    active                  =   models.BooleanField(default=True)
    user_register           =   models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    user_update             =   models.ForeignKey(UserProfile, on_delete = models.CASCADE, null=True, related_name = "user_update_an")
    type_action             =   models.ForeignKey(TypeAction, related_name = "typea", on_delete= models.CASCADE, null=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=True)



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
    date_update         =   models.DateTimeField(null=True, blank=True)
    active              =   models.BooleanField(default=True)
    publication = models.ForeignKey('publication', on_delete=models.CASCADE, null=True)
    user_register       =   models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    user_update         =   models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_update_mul")
