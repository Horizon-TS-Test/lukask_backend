from rest_framework import serializers
import datetime

from . import models

class PersonSerializer(serializers.ModelSerializer):
    """
    A SERIALIZER FOR TODO MODEL
    """
    # UNCOMMENT NEXT LINE IF DOMAIN URL IS NOT NEEDED:
    # prod_image = serializers.ImageField(use_url=False)

    class Meta:
        model = models.Person
        fields = ('id_person', 'age', 'identification_card', 'name',
                  'last_name', 'telephone', 'address', 'active')



class UserProfileSerializer(serializers.ModelSerializer):
    """
    CALSE SERIALIZABLE PARA  OBJECTS USERPROFILE
    """
    person = PersonSerializer(read_only=True)
    personSelect = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.Person.objects.all(), source='person')
    class Meta:
        model = models.UserProfile
        fields = ('id','email', 'password', 'person', 'personSelect', 'media_profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        CREATE AND RETURN A NEW USER.
        """
        user = models.UserProfile(
            email= validated_data['email'],
            person= validated_data['person'],
            media_profile = validated_data['media_profile']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        """
        UPDATE AND RETURN A USER.
        """
        print ("datos_imagen: ", instance.media_profile)
        print ("datos_password: ", instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.person = validated_data.get('person', instance.person)
        instance.media_profile = validated_data.get('media_profile', instance.media_profile)
        instance.set_password(validated_data.get('password', instance.password))
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




class TypePublicationSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZABLE PARA EL OBJETO TYPEPUBLICATION CRUD
    """
    class Meta:
        model = models.TypePublication
        fields = ('id_type_publication','description','date_register',
                  'date_update', 'active', 'user_register', 'user_update')


class TypeActionSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZADORA PARA EL OBJETO TYPEACTION CRUD
    """
    class Meta:
        model = models.TypeAction
        fields = ('id_type_action', 'description_action', 'date_register',
                  'date_update', 'active', 'user_register', 'user_update')




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
    user_update = UserProfileSerializer(read_only=True)
    date_update_d = serializers.DateTimeField(read_only=True, source="date_update")
    class Meta:
        model = models.Multimedia
        fields = ('format_multimedia', 'id_multimedia', 'name_file', 'description_file', 'media_file',
                  'date_register', 'date_update_d', 'active', 'user_update')




class MultimediaSingleSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZADORA COMPUESTA PARA EL OBJECTO MULTIMEDIA CRUD
    """

    latitude = serializers.FloatField(write_only=True, source="publication.latitude")
    length = serializers.FloatField(write_only=True, source="publication.length")
    detail = serializers.CharField(write_only=True, source="publication.detail")
    date_publication = serializers.DateTimeField(write_only = True, source="publication.date_publication")
    type_publication = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.TypePublication.objects.all(), source='publication.type_publication')
    priority_publication = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.PriorityPublication.objects.all(), source='publication.priority_publication')
    user_register_id = serializers.IntegerField(read_only=True, source="user_register.id")

    class Meta:
        model = models.Multimedia
        fields = ('format_multimedia', 'id_multimedia', 'name_file', 'description_file', 'media_file', 'date_register',
                  'date_update', 'active','user_update', 'latitude', 'length', 'detail', 'date_publication','type_publication',
                  'priority_publication', 'user_register_id')

    def create(self, validated_data):
        """
        El metodo permite ingresar una publicacion con su los datos del archivo multimedia.
        :param validated_data:
        :return: new_multimedia retorna el objeto multimedia ingresado.
        """
        publication_data = validated_data.pop('publication')
        user_register = validated_data.get('user_register')
        publication = models.Publication(
            latitude = publication_data['latitude'],
            length = publication_data['length'],
            detail = publication_data['detail'],
            active = True,
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
        return new_multimedia


    def update(self, instance, validated_data):
            instance.user_update = validated_data.get("user_update")
            instance.save()
            return  instance




class PublicationSerializer(serializers.ModelSerializer):
   """
   CLASE SERIALIZADORA PARA EL OBJECTO PUBLICATION CRUD
   """

   medios_data = MultimediaSerializer(write_only=True, many=True, required=True)
   medios = MultimediaSerializer(read_only=True, many=True)
   user_name = serializers.CharField(read_only=True, source="user_register.person.name")
   user_lastname = serializers.CharField(read_only=True, source="user_register.person.last_name")
   user_email = serializers.CharField(read_only=True, source="user_register.email")
   media_profile = serializers.ImageField(read_only=True, source="user_register.media_profile")
   priority_publication_detail = serializers.CharField(read_only=True, source="priority_publication.description")
   type_publication_detail = serializers.CharField(read_only=True, source="type_publication.description")
   user_update = UserProfileSerializer(read_only=True, many=True)

   class Meta:
      model = models.Publication
      fields = ('id_publication', 'latitude', 'length', 'detail', 'date_publication', 'date_register',
                'date_update', 'priority_publication', 'priority_publication_detail', 'type_publication', 'active',
                'type_publication_detail', 'activity', 'user_update', 'medios', 'user_name', 'user_lastname',
                'user_email', 'media_profile', 'medios_data')

   def create(self, validated_data):
        medios = validated_data.pop('medios_data')
        user_reg = validated_data.get('user_register')
        publication_info = models.Publication.objects.create(**validated_data)
        if medios is not None:
            for medio in medios:
                print("medio .....after insert", medio)
                models.Multimedia.objects.create(publication = publication_info, user_register = user_reg,  **medio)
        return publication_info




class ActionSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZADORA PARA EL OBJECTO ACTION sCRUD
    """

    type_action = TypeActionSerializer(read_only=True)
    typeactionSelect = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.TypeAction.objects.all(), source='type_action')
    publication = PublicationSerializer(read_only=True)
    publicationSelect = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.Publication.objects.all(), source='publication')

    class Meta:
        model = models.ActionNotification
        fields = ('id_action_notification', 'date_register', 'date_update', 'user_register',
                  'user_update', 'type_action', 'publication', 'typeactionSelect', 'publicationSelect', 'active')





