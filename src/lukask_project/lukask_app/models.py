"""
DOCUMENTACION DE ESTE MODULO.
El presente script contiene informacion sobre los modelos de la base de datos para la aplicacion LUKASK.
por medio de este escript se puede gestionar el modelo fisico de la DB para la creacion, modificacion e eliminacion
de tablas, hay que tomar en cuenta reglas de disenio de DB relacional para al momento del modelamiento de la db ya que
el modelo se creara tomando en cuenta cardinalidad sin garantizar que el proceso de migracion se lo realize correctamente
segun su disenio si no se ha definido bien los modelos de acuerdo a las reglas de DRF para persistencia de datos, para evitar incovenientes
se recomienda leer la documentacion de modelos para DRF.
"""

__author__      = "Dennys Ivan Moyón Gunsha"
__copyright__   = "Copyreight 2018, Horizon Technology Solutions"
__credits__     = ["Horizon Tecnology Solutions", "Dennys Moyón", "Patricia Allauca"]
__license__     = "GPL"
__version__     = "0.1.0"
__maintainer__  = "Consultores HTS"
__email__       = "dmoyon@horizon-ts.com"
__status__      = "Develop"

from django.db import models
# FOR AUTHENTICATION:
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.postgres.fields import JSONField
# PERMISSIONS FOR SPECIFIC USERS TO LET THEM TO DO SOMETHING:
from django.contrib.auth.models import PermissionsMixin
import uuid

# Create your models here.
# MANAGER CLASS TO HANDLE ALL MODELS:


def make_id_model():
    """
    Permite Generar UUID para los registros de la DB.
    :return: uuid clava unica para registro de la DB
    """
    return uuid.uuid4()

class UserProfileManager(BaseUserManager):
    """
    HELPS DJANGO WORK WITH UR CUSTOM USER MODEL.
    """

    def create_user(self, email, person, password=None):
        """
        CREATES A NEW USER PROFILE OBJECTS
        """

        if not email:
            raise ValueError('Users must have an email address.')

        # CONVERTS EVERY EMAIL CHARACTER TO LOWERCASE:
        # REF: https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager.normalize_email
        email = self.normalize_email(email)
        user = self.model(email=email, person = person)

        # NEXT FUNCTIONS WILL ENCRYPT PASSWORD FOR US, RETURNING A HASH TO BE
        # STORED IN OUR DATABASE:
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, person):
        """
        CREATES AND SAVES A NEW SUPERUSER WITH GIVEN DETAILS:
        """
        user = self.create_user(email, password, person)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user




#--------------------------------------------------------------------------------------#
#---------------DEFINICION DE MODELOS DE BASE DE DATOS PARA APLICACION LUKASK----------#
#--------------------------------------------------------------------------------------#
class Person(models.Model):
    """
    MODELO PERSON QUE REPRESENTA A LA TABLA lukask_app_person EN LA DB.
    """
    id_person = models.UUIDField(primary_key=True, default=make_id_model, editable=False, unique=True)
    age = models.IntegerField()
    identification_card = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=10)
    cell_phone = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=75)
    active = models.BooleanField(default=True)
    birthdate =  models.DateTimeField(null=True, blank=True)
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True, blank=True)
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
    MODELO USERPROFILE REPRESENTA A LA TABLA lukask_app_userprofile DE LA DB LUKASK_DB
    """

    # DJANGO MODELS REF: https://docs.djangoproject.com/en/1.11/topics/db/models/
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True, blank=True)
    person = models.OneToOneField('person', related_name='userProfile', on_delete=models.CASCADE, null=True)
    media_profile =  models.ImageField(upload_to='medios_profile', default='default_profile.png')
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'  # EMAIL IS REQUIRED BY DEFAULT

    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return self.email




class Profile(models.Model):
    """
    MODELOS PROFILE QUE REPRESENTA A LA TABLA lukask_app_profile  EN LA DB lukask_db
    """

    id_profile= models.UUIDField(primary_key=True, default=make_id_model, editable=False, unique=True)
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




class ProfileUser(models.Model):
    """
    MODELO PROFILEUSER REPRESENTA A LA TABLA lukask_app_profileuser DE LA DB LUKASK_DB
    """

    date_login = models.DateTimeField()
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user_register = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_register_pu")
    user_update = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null = True, related_name = "user_update_pu")




class PriorityPublication(models.Model):
    """
    MODELO PRIORITYPUBLICATION REPRESENTA A LA TABLA lukask_app_prioritypublication DE LA DB LUKASK_DB
    """

    id_priority_publication = models.UUIDField(primary_key=True, default=make_id_model, editable=False, unique=True)
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




class TypePublication(models.Model):
    """
    MODELO TYPEPUBLICATION QUE REPRESENTA A LA TABLA lukask_app_typepublication DE LA DB LUKASK_DB
    """

    id_type_publication = models.UUIDField(primary_key=True, default=make_id_model, editable=False, unique=True)
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




class Tracing(models.Model):
    """
    MODELO TRACING QUE REPRESENTA A LA TABLA lukask_app_tracing DE LA BASE DB LUKASK_DB
    """

    id_tracing = models.UUIDField(primary_key=True, default=make_id_model, editable=False, unique=True)
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
        return '%f %s' % (self.percentage_avance, self.date_start.strftime('%d-%m-%Y'))




class Activity(models.Model):
    """
    MODELO ACTIVITY QUE REPRESENTA A LA TABLA lukask_app_activity DE LA DB LUKASK_DB
    """

    id_activity = models.UUIDField(primary_key=True, default=make_id_model, editable=False, unique=True)
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




class Publication(models.Model):
    """
    MODELO PUBLICATION QUE REPRESENTA A LA TABLA lukask_app_publication DE LA DB LUKASK_DB
    """

    id_publication = models.UUIDField(primary_key=True, default=make_id_model, editable=False, unique=True)
    latitude = models.FloatField()
    length = models.FloatField()
    location = models.CharField(max_length=60, null=True)
    address  = models.CharField(max_length=100, null=True)
    detail = models.TextField(max_length= 300)
    date_publication = models.DateTimeField(null=True)
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    priority_publication = models.ForeignKey('priorityPublication', on_delete=models.CASCADE, null = True) # FK TABLE PRIORITY_PUBLICATION
    type_publication = models.ForeignKey('typePublication', on_delete=models.CASCADE, null=True) # FK TABLE TYPE_PUBLICATION
    activity = models.ForeignKey('activity', on_delete=models.CASCADE, null=True)  # FK TABLE ACTIVITY

    user_register = models.ForeignKey('userProfile', on_delete=models.CASCADE,  null=True)
    user_update = models.ForeignKey('userProfile', on_delete=models.CASCADE, null=True, related_name="user_update_pl")

    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return '%s %f %f' % (self.detail, self.latitude, self.length)

    def set_user_register(self, user_register):
        self.user_register = user_register




class TypeAction(models.Model):
    """
    MODELO TYPEACTION QUE REPRESENTA A LA TABLA lukask_app_typeaction DE LA DB LUKASK_DB
    """

    id_type_action = models.UUIDField(primary_key= True, default=make_id_model, editable= False, unique=True)
    description_action  =   models.CharField(max_length=75)
    date_register       =   models.DateTimeField(auto_now_add = True)
    date_update         =   models.DateTimeField(null=True, blank=True)
    active              =   models.BooleanField(default=True)
    user_register       =   models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    user_update         =   models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_update_ta")


    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return self.description_action




class ActionPublication(models.Model):
    """
    MODELO ACTIONNOTIFICATION QUE REPRESENTA A LA TABLA lukak_app_actionnotification  DE LA DB LUKASK_DB
    """

    id_action               =   models.UUIDField(primary_key = True, default=make_id_model, editable = False, unique=True)
    date_register           =   models.DateTimeField(auto_now_add = True, null=True)
    date_update             =   models.DateTimeField(null=True, blank=True)
    description             =   models.CharField(max_length=500, null=True)
    active                  =   models.BooleanField(default=True)
    user_register           =   models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_update             =   models.ForeignKey(UserProfile, on_delete = models.CASCADE, null=True, related_name = "user_update_an")
    type_action             =   models.ForeignKey(TypeAction, related_name = "typea", on_delete= models.CASCADE, null=True)
    publication             =   models.ForeignKey(Publication,  related_name='actionPublication', on_delete=models.CASCADE, null=True)
    action_parent           =   models.ForeignKey('self', null=True)


    def __str__(self):
        _data = self.description
        if _data is None:
            _data = "default"
        return _data


class Multimedia(models.Model):
    """
    MODELO MULTIMEDIA QUE REPRESENTA A LA TABLA  lukask_app_multimedia DE LA DB LUKASK_DB
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
    id_multimedia       =   models.UUIDField(primary_key=True, unique=True, default=make_id_model, editable = False)
    name_file           =   models.CharField(max_length=50, null=True)
    description_file    =   models.CharField(null=True, max_length=50)
    media_file          =   models.ImageField(upload_to='medios', default='default.jpg')
    date_register       =   models.DateTimeField(auto_now_add = True)
    date_update         =   models.DateTimeField(null=True, blank=True)
    active              =   models.BooleanField(default=True)
    publication         =   models.ForeignKey('publication', related_name='medios', on_delete=models.CASCADE, null=True)
    user_register       =   models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    user_update         =   models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_update_mul")
    actionPublication   =   models.ForeignKey('actionpublication', related_name='mediosactionPub', on_delete=models.CASCADE, null=True)


class Notification(models.Model):
    """
    MODELO NOTIFICACION QUE REPRESENTA A LA TABLA lukask_app_notification DE LA DB LUKASK_DB
    """
    id_notification             = models.UUIDField(primary_key=True, unique=True, default=make_id_model, editable=False)
    description_notification    = models.CharField(max_length=100, null=True)
    date_register               = models.DateTimeField(auto_now_add = True)
    date_generated_notification = models.DateTimeField(null = True, blank = True)
    user_register               = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    active                      = models.BooleanField(default=True)
    users_notificated           = models.ManyToManyField(UserProfile, through='NotificationReceived', related_name="usernotificated")

    def __str__(self):
        return self.description_notification


class NotificationReceived(models.Model):
    """
    MODELO NOTIFICAIONES RECIBIDAS QUE REPRESENTA A LA TABLA lukask_app_notificationreceived DE LA LUKASK_DB
    """
    description_notif_rec       = models.CharField(max_length=100, null = True)
    user_received               = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='userreceived')
    notification                = models.ForeignKey(Notification, on_delete=models.CASCADE, null=True, related_name='notification')
    date_register               = models.DateTimeField(auto_now_add= True)
    active                      = models.BooleanField(default=True)

