import datetime
import json

from rest_framework import serializers
from .lukask_constants import LukaskConstants

from . import models

class ProvinceSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZERIALIZADORA PARA MODELO PROVINCE
    """
    cantons = serializers.SerializerMethodField()

    class Meta:
        model  = models.Province
        fields = ('id_province', 'description_province', 'date_register', 'cantons')
        read_only_fields = ('data_register', )


    def get_cantons(self, obj):
        """
        Obtenemos todos las parroquias del canton
        :param obj:
        :return:
        """
        cantons_data = models.Canton.objects.filter(province = obj.id_province)
        data_province   = []

        for item_canton in cantons_data:
            item_json = '{}'
            item_json = json.loads(item_json)
            item_json["description_canton"]= item_canton.description_canton
            item_json["id_canton"]= item_canton.id_canton
            data_province.append(item_json)

        return data_province


class CantonSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZERIALIZADORA PARA MODELO CANTON
    """
    parishs = serializers.SerializerMethodField()
    class Meta:
        model  = models.Canton
        fields = ('id_canton', 'description_canton', 'date_register', 'province', 'parishs')
        read_only_fields = ('data_register', )

    def get_parishs(self, obj):
        """
        Obtenemos todos los datos de las parroquias
        :param obj:
        :return:
        """
        parish_data = models.Parish.objects.filter(canton = obj.id_canton)
        data_parish = []

        for item_parish in parish_data:
            item_json = '{}'
            item_json = json.loads(item_json)
            item_json["description_"] = item_parish.description_parish
            item_json["id_canton"] = item_parish.id_parish
            data_parish.append(item_json)

        return data_parish


class ParishSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZERIALIZADORA PARA MODELO CANTON
    """
    class Meta:
        model  = models.Parish
        fields = ('id_parish', 'description_parish', 'date_register', 'canton')
        read_only_fields = ('data_register', )


class PersonSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZER FOR TODO MODEL
    """
    # UNCOMMENT NEXT LINE IF DOMAIN URL IS NOT NEEDED:
    # prod_image = serializers.ImageField(use_url=False)

    class Meta:
        model = models.Person
        fields = ('id_person', 'age', 'identification_card', 'name', 'last_name', 'telephone', 'cell_phone', 'birthdate',
                  'address', 'active', 'date_register', 'date_update', 'parish')
        read_only_fields = ('active', 'date_register', 'date_update')



class UserProfileSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZABLE PARA  OBJECTS USERPROFILE
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
        instance.person.parish                  = person.get("parish", instance.person.parish)
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
    receivers = serializers.SerializerMethodField()
    pub_owner = serializers.SerializerMethodField()
    action_parent_owner = serializers.SerializerMethodField()

    class Meta:
        model = models.ActionPublication
        fields = ('id_action', 'description', 'date_register', 'date_update', 'user_update', 'type_action',
                  'publication', 'pub_owner', 'action_parent', 'action_parent_owner','active', 'mediosactionPub', 'name_file', 'format_multimedia', 'media_file',
                  'user_register', 'receivers')
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


    def get_receivers(self, obj):

        from django.core import serializers
        users_register = None

        #Owners de la publicacion y comentario
        owner_publication = obj.publication
        owner_commet = None

        #Si es una comentario a la Publicacio
        if obj.publication is not None and obj.action_parent is None:
            users_register =  models.ActionPublication.objects.filter(
                type_action__description_action =  LukaskConstants.TYPE_ACTION_COMMENTS,
                publication = obj.publication, action_parent = None).exclude(user_register__id = obj.user_register.id).order_by(
                'user_register').distinct('user_register')

        #Si es una respuesta de un comentario
        elif obj.publication is not None and obj.action_parent is not None:

            owner_commet = obj.action_parent
            users_register = models.ActionPublication.objects.filter(
                type_action__description_action=LukaskConstants.TYPE_ACTION_COMMENTS,
                publication=obj.publication, action_parent = obj.action_parent).exclude(user_register__id=obj.user_register.id).order_by(
                'user_register').distinct('user_register')

            #usuarios a notificar
            users_register = list(users_register)
            if not users_register and obj.user_register != owner_commet.user_register:
                users_register.append(owner_commet)
            elif users_register:

                #Validamos que el usuario creador dela notificcion este en la lista
                user_owner_in_notif = next((item for item in users_register if  item.user_register == owner_commet.user_register), None)
                users_register.append(owner_commet)
                print ("user_owner_in_notif....", user_owner_in_notif)

        #Todos los acciones que interactuan con la publicacion
        else:
            users_register = models.ActionPublication.objects.filter(publication = obj.publication).exclude(
                user_register__id=obj.user_register.id).order_by('user_register').distinct('user_register')


        #Validamos si existen  usuarios que han comentado
        data_json = None
        if not users_register and obj.user_register != owner_publication.user_register:
            list_pub = []
            list_pub.append(obj.publication)
            data_json = serializers.serialize('json', list_pub, fields =('user_register',))
        else :
            data_json = serializers.serialize('json', users_register, fields=('user_register',))


        #Convetimos a formato Json
        users_received = json.loads(data_json)
        
        #Validamos propietario del la publicacion
        in_list_owner = False
        for item_user in users_received:

            id_usr = int(item_user["fields"]["user_register"])
            #user =list(models.UserProfile.objects.filter(id = id_usr).values('person__name', 'person__last_name'))
            #user_name = user[0].get('person__name')
            #user_lastname =  user[0].get('person__last_name')
            item_user["fields"]["owner_publication"] = False
            item_user["fields"]["owner_commet"] = False
            #item_user["fields"]["user_name"] = user_name
            #item_user["fields"]["user_lastname"] = user_lastname

            #esta en lista el duenio de la publicacion
            if id_usr == owner_publication.user_register.id :
                in_list_owner = True
                item_user["fields"]["owner_publication"] = True

            #esta en lista el duenio del comentario
            if owner_commet is not None and id_usr == owner_commet.user_register.id :
                item_user["fields"]["owner_commet"] = True


        #Verificamos que el que el que realizo la publicacion se encuentre en la lista.
        if not in_list_owner and obj.user_register != owner_publication.user_register:
            json_owner = {"fields": {"user_register": obj.publication.user_register.id, "user_lastname": obj.publication.user_register.person.last_name,
                          "user_name" : obj.publication.user_register.person.name, "owner_publication" : True, "owner_commet": False}}
            users_received.append(json_owner)


        return  users_received

    def get_action_parent_owner(self, obj):
        """
        Obtenemos los datos de la accion padre
        :param obj:
        :return: format_action_parent
        """
        format_action_parent = '{}'
        format_action_parent  = json.loads(format_action_parent)
        if obj.action_parent:
            format_action_parent["owner"] = True
            format_action_parent["id"] = obj.action_parent.user_register.id
            format_action_parent["user_name"] = obj.action_parent.user_register.person.name
            format_action_parent["user_lastname"] = obj.action_parent.user_register.person.last_name
        return  format_action_parent

    def get_pub_owner(self, obj):
        """
        Obtenemos los datos la publicacion
        :param obj:
        :return: format_publication
        """
        format_publication = '{}'
        format_publication = json.loads(format_publication)
        format_publication["user_id"] = obj.publication.user_register.id
        format_publication["user_name"] = obj.publication.user_register.person.name
        format_publication["user_lastname"] = obj.publication.user_register.person.last_name
        format_publication["owner"] = True
        return format_publication


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
    url       = serializers.CharField(read_only = True, source = "notification.url")
    class Meta:
        model = models.NotificationReceived
        fields  = ('description_notif_rec', 'user_received', 'notification', 'date_register', 'url', 'user_emit')
        read_only_fields = ('date_register',)


class NotificationSerializer(serializers.ModelSerializer):
    """
     CLASE SERIALIZADORA  PARA EL OBJETO NOTIFICATION CRUD
    """
    user_register = UserProfileSerializer(read_only=True)
    users_notificated = NotificationReceivedSerializer(many=True, write_only=True)

    class Meta:
        model  = models.Notification
        fields = ('id_notification', 'description_notification', 'date_register', 'date_generated', 'url', 'user_register','active', 'users_notificated')
        read_only_fields = ('date_register', 'active')

    def create(self, validated_data):
        print("validated_data", validated_data)
        date_generated  = validated_data.get('date_generated', None)
        notifs_received = validated_data.pop("users_notificated", None)
        notification =  models.Notification.objects.create(**validated_data)
        print ("date_generated", date_generated)
        if notifs_received is not None:
            for notif_received in notifs_received:
                models.NotificationReceived.objects.create(date_register = date_generated, notification = notification, **notif_received)
        return notification


