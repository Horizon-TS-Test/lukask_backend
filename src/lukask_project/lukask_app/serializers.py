import datetime

from rest_framework import serializers
from .lukask_constants import LukaskConstants

from . import models

class PersonSerializer(serializers.ModelSerializer):
    """
    A SERIALIZER FOR TODO MODEL
    """
    # UNCOMMENT NEXT LINE IF DOMAIN URL IS NOT NEEDED:
    # prod_image = serializers.ImageField(use_url=False)

    class Meta:
        model = models.Person
        fields = ('id_person', 'age', 'identification_card', 'name', 'last_name', 'telephone', 'cell_phone', 'birthdate',
                  'address', 'active', 'date_register', 'date_update')
        read_only_fields = ('active', 'date_register', 'date_update')



class UserProfileSerializer(serializers.ModelSerializer):
    """
    CALSE SERIALIZABLE PARA  OBJECTS USERPROFILE
    """
    person = PersonSerializer()
    #personSelect = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.Person.objects.all(), source='person')
    class Meta:
        model = models.UserProfile
        fields = ('id','email', 'password','media_profile', 'date_update', 'is_active', 'person')
        read_only_fields = ("date_uodate",)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        CREATE AND RETURN A NEW USER.
        """
        _data_person = validated_data.pop('person')
        person = models.Person.objects.create(**_data_person)
        user = models.UserProfile(
            email= validated_data['email'],
            person= person,
            media_profile = validated_data['media_profile']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        """
        UPDATE AND RETURN A USER.
        """
        person = validated_data.get("person")
        instance.email                          = validated_data.get('email', instance.email)
        instance.media_profile                  = validated_data.get('media_profile', instance.media_profile)
        instance.is_active                      = validated_data.get('is_active', instance.is_active)
        instance.date_update                    = datetime.datetime.now()
        if validated_data.get('password') is not None:
            instance.set_password(validated_data.get('password', instance.password))
        instance.person.age                     = person.get("age", instance.person.age)
        instance.person.identification_card     = person.get("identification_card", instance.person.identification_card)
        instance.person.name                    = person.get("name", instance.person.name)
        instance.person.last_name               = person.get("last_name", instance.person.last_name)
        instance.person.telephone               = person.get("telephone", instance.person.telephone)
        instance.person.cell_phone              = person.get("cell_phone", instance.person.cell_phone)
        instance.person.birthdate               = person.get("birthdate", instance.person.birthdate)
        instance.person.address                 = person.get("address", instance.person.address)
        instance.person.active                  = validated_data.get('is_active', instance.is_active)
        instance.person.date_update             = datetime.datetime.now()
        instance.person.save()
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZABLE PARA EL OBJETO PROFILE CRUD
    """
    class Meta:
       model = models.Profile
       fields = ('id_profile', 'description', 'date_register', 'date_update',
                  'active', 'user_register', 'user_update', 'users')



class ProfileUserSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZABLE PARA EL OBJETO PROFILEUSER CRUD
    """
    class Meta:
        model = models.ProfileUser
        fields = ('date_login', 'date_register', 'date_update', 'active', 'user',
                  'profile', 'user_register', 'user_update')



class PriorityPublicationSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZABLE PARA EL OBJETO PRIORITYPUBLICATION CRUD
    """
    class Meta:
        model = models.PriorityPublication
        fields = ('id_priority_publication', 'description', 'date_register',
                  'date_update', 'active', 'user_register', 'user_update')
        read_only_fields = ('user_register', 'active')




class TypePublicationSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZABLE PARA EL OBJETO TYPEPUBLICATION CRUD
    """
    class Meta:
        model = models.TypePublication
        fields = ('id_type_publication','description','date_register',
                  'date_update', 'active', 'user_register', 'user_update')
        read_only_fields  = ('active', 'user_register')


class TypeActionSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZADORA PARA EL OBJETO TYPEACTION CRUD
    """
    class Meta:
        model = models.TypeAction
        fields = ('id_type_action', 'description_action', 'date_register',
                  'date_update', 'active', 'user_register', 'user_update')
        read_only_fields = ('user_register','data_register', 'active')



class TracingSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZADORA PARA EL OBJETO TRACING CRUD
    """
    class Meta:
        model = models.Tracing
        fields = ('id_tracing', 'percentage_avance', 'date_start', 'estimated_end_date',
                  'real_end_date', 'date_register', 'date_update', 'active', 'publication',
                  'user_register', 'user_update')



class ActivitySerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZADORA PARA EL OBJETO ACTIVITY CRUD
    """
    class Meta:
        model = models.Activity
        fields = ('id_activity', 'description_activity', 'estimated_start_date', 'real_start_date', 'estimated_end_date',
                  'real_end_date', 'date_register', 'date_update', 'published', 'active', 'tracing', 'user_register', 'user_update')




class MultimediaSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZADORA SIMPLE PARA EL OBJETO MULTIMEDIA CRUD
    """
    id_publication = serializers.UUIDField(read_only=True, source='publication.id_publication')
    class Meta:
        model = models.Multimedia
        fields = ('id_publication','format_multimedia', 'id_multimedia', 'name_file', 'description_file', 'media_file',
                  'date_register', 'date_update', 'active', 'user_update', 'user_register', 'actionPublication')
        read_only_fields = ('user_register', 'actionPublication', 'active')




class MultimediaSingleSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZADORA COMPUESTA PARA EL OBJECTO MULTIMEDIA CRUD
    """

    #latitude = serializers.FloatField(write_only=True, source="publication.latitude")
    #length = serializers.FloatField(write_only=True, source="publication.length")
    #detail = serializers.CharField(write_only=True, source="publication.detail")
    #date_publication = serializers.DateTimeField(write_only = True, source="publication.date_publication")
    #type_publication = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.TypePublication.objects.all(), source='publication.type_publication')
    #priority_publication = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.PriorityPublication.objects.all(), source='publication.priority_publication')
    #user_register_id = serializers.IntegerField(read_only=True, source="user_register.id")
    multimedia = MultimediaSerializer(write_only=True, many=True)
    class Meta:
        model = models.Multimedia
        fields = ('publication', 'id_multimedia', 'format_multimedia', 'name_file', 'media_file','multimedia', 'active')
        read_only_fields = ('format_multimedia', 'id_multimedia', 'name_file', 'media_file', 'active')

    def create(self, validated_data):
        """
        Proceso para adicionar imagenes a la publicacion
        :param validated_data:
        :return:
        """
        _publication = validated_data.pop('publication')
        _medios  = validated_data.pop('multimedia')
        _user_register = validated_data.pop('user_register')
        _medio = None
        if _medios is not None:
            for medio in _medios:
                _medio = models.Multimedia.objects.create(publication = _publication, user_register = _user_register, **medio)
        return _medio



    """def create(self, validated_data):
        
        publication_data = validated_data.pop('publication')
        user_register = validated_data.get('user_register')
        publication = models.Publication(
            latitude = publication_data['latitude'],
            length = publication_data['length'],
            detail = publication_data['detail'],
            active = LukaskConstants.LOGICAL_STATE_ACTIVE,
            date_publication =  publication_data['date_publication'],
            type_publication = publication_data['type_publication'],
            priority_publication = publication_data['priority_publication'],
            user_register = user_register,
            date_register = datetime.datetime.now()
        )

        #Guarda la publicacion.
        publication.save()

        #Guarda y asigna la publicacion  al archivo multimedia.
        new_multimedia = models.Multimedia(
            media_file = validated_data['media_file'],
            description_file = validated_data['description_file'],
            name_file = validated_data['name_file'],
            active = True,
            format_multimedia = validated_data['format_multimedia'],
            publication = publication,
            user_register=user_register,
            date_register=datetime.datetime.now()
        )
        new_multimedia.save()
        return new_multimedia"""


    """def update(self, instance, validated_data):
            instance.user_update = validated_data.get("user_update")
            instance.save()
            return  instance"""



class ActionSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZADORA PARA EL OBJECTO ACTION sCRUD
    """
    name_file = serializers.CharField(write_only=True, source="multimedia.name_file", required=False)
    format_multimedia = serializers.CharField(write_only=True, source="multimedia.format_multimedia", required=False)
    media_file = serializers.FileField(write_only=True, source="multimedia.media_file", required=False)
    mediosactionPub = MultimediaSerializer(read_only=True, many=True)
    user_register = UserProfileSerializer(read_only=True)
    received = serializers.SerializerMethodField()

    class Meta:
        model = models.ActionPublication
        fields = ('id_action', 'description', 'date_register', 'date_update', 'user_update', 'type_action',
                  'publication','action_parent', 'active', 'mediosactionPub', 'name_file', 'format_multimedia', 'media_file',
                  'user_register', 'received')
        read_only_fields = ('date_register', 'user_register')


    def create(self, validated_data):
        """
        Permite la creacion de acciones sobre la publicacion, actualiza o crea una accion,
        simpre y cuando sea de tipo relevancia.
        :param validated_data:
        :return:
        """
        _user_register = validated_data.get('user_register')
        _publication = validated_data.get('publication')
        _type_action = validated_data.get('type_action')
        _action_publication_update_or_create = None

        if _type_action.description_action == LukaskConstants.TYPE_ACTION_RELEVANCE:

            #Valia si existe ya alguna accion de tipo relevancia
            try:
                _action_publication_update_or_create = models.ActionPublication.objects.get(user_register = _user_register, publication = _publication,
                                                                                        type_action__description_action = LukaskConstants.TYPE_ACTION_RELEVANCE)

                #Actualiza
                _action_publication_update_or_create.date_update = datetime.datetime.now()
                _action_publication_update_or_create.user_update = _user_register
                _action_publication_update_or_create.active = validated_data.get('active', False)
                _action_publication_update_or_create.save()
                return  _action_publication_update_or_create

            except models.ActionPublication.DoesNotExist:

                #Crea
                _action_publication_update_or_create = models.ActionPublication()
                for key, value in validated_data.items():
                    setattr(_action_publication_update_or_create, key, value)
                _action_publication_update_or_create.save()
                return  _action_publication_update_or_create

        else:

            #Crea una accion que no sea de tipo relevancia.
            _multimedia_publication = validated_data.pop('multimedia', None)
            _action_publication_update_or_create = models.ActionPublication.objects.create(**validated_data)

            if _multimedia_publication is not None:
                models.Multimedia.objects.create(actionPublication = _action_publication_update_or_create, user_register = _user_register, **_multimedia_publication)
            print ("_action_publication_update_or_create....", _action_publication_update_or_create)
        return _action_publication_update_or_create


    def get_received(self, obj):

        from django.core import serializers
        users_register = None

        #Si es una comentario a la Publicacio
        if obj.publication is not None and obj.action_parent is None:
            users_register =  models.ActionPublication.objects.filter(
                type_action__description_action =  LukaskConstants.TYPE_ACTION_COMMENTS,
                publication = obj.publication, action_parent = None).exclude(user_register__id = obj.user_register.id).order_by(
                'user_register').distinct('user_register')

        #Si es una respuesta de un comentario
        elif obj.publication is not None and obj.action_parent is not None:
            users_register = models.ActionPublication.objects.filter(
                type_action__description_action=LukaskConstants.TYPE_ACTION_COMMENTS,
                publication=obj.publication, action_parent = obj.action_parent).exclude(user_register__id=obj.user_register.id).order_by(
                'user_register').distinct('user_register')

        #Todos los acciones que interactuan con la publicacion
        else:
            users_register = models.ActionPublication.objects.filter(publication = obj.publication).exclude(
                user_register__id=obj.user_register.id).order_by('user_register').distinct('user_register')
        print ("users_register......", users_register)
        return  serializers.serialize('json', users_register, fields=('user_register',))


class PublicationSerializer(serializers.ModelSerializer):
   """
   CLASE SERIALIZADORA PARA EL OBJECTO PUBLICATION CRUD
   """

   medios_data = MultimediaSerializer(write_only=True, many=True, required=True)
   medios = MultimediaSerializer(read_only=True, many=True)
   priority_publication_detail = serializers.CharField(read_only=True, source="priority_publication.description")
   type_publication_detail = serializers.CharField(read_only=True, source="type_publication.description")
   user_update = UserProfileSerializer(read_only=True)
   user_register = UserProfileSerializer(read_only=True)
   count_relevance = serializers.SerializerMethodField()
   user_relevance = serializers.SerializerMethodField()

   class Meta:
      model = models.Publication
      fields = ('id_publication', 'latitude', 'length', 'detail', 'location', 'date_publication', 'date_register',
                'date_update', 'priority_publication', 'priority_publication_detail', 'type_publication', 'active',
                'type_publication_detail', 'activity', 'user_update', 'address', 'medios', 'medios_data', 'user_register', 'count_relevance',
                'user_relevance')
      read_only_fields  = ('active', )

   def create(self, validated_data):
        print("validated_data...........", validated_data)
        medios = validated_data.pop('medios_data')
        user_reg = validated_data.get('user_register')
        publication_info = models.Publication.objects.create(**validated_data)
        if medios is not None:
            if len(medios) > 0:
                print ("con datos para multimedia")
                for medio in medios:
                    print("medio .....after insert", medio)
                    models.Multimedia.objects.create(publication = publication_info, user_register = user_reg,  **medio)
            else:
                print ("sin datos para multimedia")
                descripcion = validated_data.get('detail')
                models.Multimedia.objects.create(format_multimedia  = 'IG', name_file = 'Default', description_file = descripcion[0:48], publication = publication_info )

        return publication_info

   def update(self, instance, validated_data):
        instance.user_update    = validated_data.get("user_update", instance.user_update)
        instance.latitude       = validated_data.get("latitude", instance.latitude)
        instance.length         = validated_data.get("length", instance.length)
        instance.detail         = validated_data.get("detail", instance.detail)
        instance.date_publication = validated_data.get("date_publication", instance.date_publication)
        instance.date_update    = validated_data.get("date_update", instance.date_update)
        instance.active         = validated_data.get("active", instance.active)
        instance.priority_publication = validated_data.get("priority_publication", instance.priority_publication)
        instance.type_publication = validated_data.get("type_publication", instance.type_publication)
        instance.address        = validated_data.get("address", instance.address)
        instance.activity = validated_data.get("activity", instance.activity)
        instance.location  = validated_data.get("location", instance.location)
        instance.save()
        return instance

   def get_count_relevance(self, obj):
       """
       Obtiene la cantidad de relevancia q se han dado sobre una publicacion
       :param obj:
       :return: interger
       """
       return obj.actionPublication.filter(type_action__description_action=LukaskConstants.TYPE_ACTION_RELEVANCE).exclude(publication = None).count()

   def get_user_relevance(self, obj):
       """
       Verifica que el usuario en sesion, dio relevancia a una publicacion, este proceso lo hace registro por registro.
       :param obj:
       :return: boolean
       """
       user = self.context.get("user")
       publication = obj.actionPublication.filter(type_action__description_action=LukaskConstants.TYPE_ACTION_RELEVANCE, user_register__email = user,
                                                  action_parent = None, active = True).exclude(publication = None)
       if not publication:
           return False
       return True

class NotificationReceivedSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZADORA PARA EL OBJETO NOTIFICATIONRECEIVED CRUD
    """
    user_emit = UserProfileSerializer(read_only = True, source = "notification.user_register")
    class Meta:
        model = models.NotificationReceived
        fields  = ('description_notif_rec', 'user_received', 'notification', 'date_register', 'user_emit')
        read_only_fields = ('date_register',)


class NotificationSerializer(serializers.ModelSerializer):
    """
     CLASE SERIALIZADORA  PARA EL OBJETO NOTIFICATION CRUD
    """
    user_register = UserProfileSerializer(read_only=True)
    users_notificated = NotificationReceivedSerializer(many=True, write_only=True)

    class Meta:
        model  = models.Notification
        fields = ('id_notification', 'description_notification', 'date_register', 'date_generated', 'user_register','active', 'users_notificated')
        read_only_fields = ('date_register', 'active')

    def create(self, validated_data):
        print("validated_data", validated_data)
        date_generated  = validated_data.get('date_generated', None)
        notifs_received = validated_data.pop("users_notificated", None)
        notification =  models.Notification.objects.create(**validated_data)
        if notifs_received is not None:
            for notif_received in notifs_received:
                models.NotificationReceived.objects.create(date_register = date_generated, notification = notification, **notif_received)
        return notification



