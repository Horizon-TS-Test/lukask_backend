from rest_framework import serializers

from . import models

class UserProfileSerializer(serializers.ModelSerializer):
    """
    A SERIALIZER FOR OUR USER PROFILE OBJECTS.
    """

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password', 'cedula')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        CREATE AND RETURN A NEW USER.
        """
        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        """
        UPDATE AND RETURN A USER.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()

        return instance


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



class Profile(serializers.ModelSerializer):
    class Meta:
        models = models.Profile
        fields = ('id_profile', 'description', 'date_register', 'date_update',
                  'active', 'user_register', 'user_update', 'users')




