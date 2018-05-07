from rest_framework import serializers

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
    A SERIALIZER FOR OUR USER PROFILE OBJECTS.
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
    class Meta:
       model = models.Profile
       fields = ('id_profile', 'description', 'date_register', 'date_update',
                  'active', 'user_register', 'user_update', 'users')



class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfileUser
        fields = ('date_login', 'date_register', 'date_update', 'active', 'user',
                  'profile', 'user_register', 'user_update')


class PriorityPublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PriorityPublication
        fields = ('id_priority_publication', 'description', 'date_register',
                  'date_update', 'active', 'user_register', 'user_update')


class TypePublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TypePublication
        fields = ('id_type_publication','description','date_register',
                  'date_update', 'active', 'user_register', 'user_update')


class TypeActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TypeAction
        fields = ('id_type_action', 'description_action', 'date_register',
                  'date_update', 'active', 'user_register', 'user_update')


class TracingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tracing
        fields = ('id_tracing', 'percentage_avance', 'date_start', 'estimated_end_date',
                  'real_end_date', 'date_register', 'date_update', 'active', 'publication',
                  'user_register', 'user_update')



class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = ('id_activity', 'description_activity', 'estimated_start_date', 'real_start_date',
              'estimated_end_date', 'real_end_date', 'date_register', 'date_update', 'published',
              'active', 'tracing', 'user_register', 'user_update')

class MultimediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Multimedia
        fields = ('format_multimedia', 'id_multimedia', 'name_file', 'description_file', 'media_file', 'date_register',
                  'date_update', 'active', 'user_register', 'user_update')

class MultimediaSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Multimedia
        fields = ('format_multimedia', 'id_multimedia', 'name_file', 'description_file', 'media_file', 'date_register',
                  'date_update', 'active', 'publication', 'user_register', 'user_update')

class PublicationSerializer(serializers.ModelSerializer):
   medios_data = MultimediaSerializer(write_only=True)
   medios = MultimediaSerializer(read_only=True, many=True)
   user_name = serializers.CharField(read_only=True, source="user_register.person.name")
   user_lastname = serializers.CharField(read_only=True, source="user_register.person.last_name")
   user_email = serializers.CharField(read_only=True, source="user_register.email")
   media_profile = serializers.ImageField(read_only=True, source="user_register.media_profile")
   priority_publication_detail = serializers.CharField(read_only=True, source="priority_publication.description")
   type_publication_detail = serializers.CharField(read_only=True, source="type_publication.description")

   class Meta:
      model = models.Publication
      fields = ('id_publication', 'latitude', 'length', 'detail', 'date_publication', 'date_register',
                'date_update', 'active', 'priority_publication_detail', 'type_publication_detail', 'activity',
                'user_register', 'user_update', 'medios','medios_data', "user_name", "user_lastname", "user_email", "media_profile")

   def create(self, validated_data):
        media_data = validated_data.pop('medios_data')
        publication_info = models.Publication.objects.create(**validated_data)
        models.Multimedia.objects.create(publication = publication_info, **media_data)
        return publication_info



class ActionSerializer(serializers.ModelSerializer):
    type_action = TypeActionSerializer(read_only=True)
    typeactionSelect = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.TypeAction.objects.all(), source='type_action')
    publication = PublicationSerializer(read_only=True)
    publicationSelect = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.Publication.objects.all(), source='publication')

    class Meta:
        model = models.ActionNotification
        fields = ('id_action_notification', 'date_register', 'date_update', 'active', 'user_register',
                  'user_update', 'type_action', 'publication', 'typeactionSelect', 'publicationSelect')


        def create(self, validated_data):
            """
            CREATE AND RETURN A NEW USER.
            """
            user = models.ActionNotification(

            )

            user.save()

            return user



