"""from django.http import Http404
from django.shortcuts import render"""

# Create your views here.
from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
"""from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView"""

from . import serializers
from . import models

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, RETRIEVEING, UPDATING AND DELETING PROFILES.
    """

    serializer_class = serializers.UserProfileSerializer
    ##permission_classes = (permissions.UdateOwnProfile, IsAuthenticated)

    queryset = models.UserProfile.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')

    authentication_classes = (TokenAuthentication,)


class PersonViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, RETRIEVEING, UPDATING AND DELETING PROFILES.
    """

    serializer_class = serializers.PersonSerializer
    ##permission_classes = (permissions.UdateOwnProfile, IsAuthenticated)

    queryset = models.Person.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('identification_card', 'name', 'last_name')

    authentication_classes = (TokenAuthentication,)


class LoginViewSet(viewsets.ViewSet):
    """
    CHECK email AND password AND RETURNS AN AUTH TOKEN
    """

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """
        USE THE ObtainedAuthToken APIView TO VALIDATE AND CREATE A TOKEN.
        """

        return ObtainAuthToken().post(request)



class TypeActionViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, READING AND UPDATING TODOS.
    """
    serializer_class = serializers.ProfileSerializer
    queryset = models.TypeAction.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description_action')

    authentication_classes = (TokenAuthentication,)



class ActionViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, READING AND UPDATING TODOS.
    """
    serializer_class = serializers.ProfileSerializer
    queryset = models.ActionNotification.objects.all()
    filter_backends = (filters.SearchFilter,)
    #search_fields = ('description_action')

    authentication_classes = (TokenAuthentication,)