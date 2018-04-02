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
    serializer_class = serializers.TypeActionSerializer
    queryset = models.TypeAction.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description_action')

    authentication_classes = (TokenAuthentication,)



class ActionViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, READING AND UPDATING TODOS.
    """
    serializer_class = serializers.ActionSerializer
    queryset = models.ActionNotification.objects.all()
    filter_backends = (filters.SearchFilter,)
    #search_fields = ('description_action')

    authentication_classes = (TokenAuthentication,)

class PriorityPublicationViewSet(viewsets.ModelViewSet):
    """"
    HANDLES CREATING, READING AND UPDATING TODOS.
        """
    serializer_class = serializers.PriorityPublicationSerializer
    queryset = models.PriorityPublication.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description')

    authentication_classes = (TokenAuthentication,)

class TypePublicationViewSet(viewsets.ModelViewSet):
    """"
    HANDLES CREATING, READING AND UPDATING TODOS.
        """
    serializer_class = serializers.TypePublicationSerializer
    queryset = models.TypePublication.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description')

    authentication_classes = (TokenAuthentication,)


class TracingViewSet(viewsets.ModelViewSet):
    """"
    HANDLES CREATING, READING AND UPDATING TODOS.
        """
    serializer_class = serializers.TracingSerializer
    queryset = models.Tracing.objects.all()
    filter_backends = (filters.SearchFilter,)
    #search_fields = ('description')

    authentication_classes = (TokenAuthentication,)


class ActivityViewSet(viewsets.ModelViewSet):
    """"
    HANDLES CREATING, READING AND UPDATING TODOS.
        """
    serializer_class = serializers.ActivitySerializer
    queryset = models.Activity.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description_activity')

    authentication_classes = (TokenAuthentication,)


class PublicationViewSet(viewsets.ModelViewSet):
    """"
    HANDLES CREATING, READING AND UPDATING TODOS.
        """
    serializer_class = serializers.PublicationSerializer
    queryset = models.Publication.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('detail')

    authentication_classes = (TokenAuthentication,)


class MultimediaViewSet(viewsets.ModelViewSet):
    """"
    HANDLES CREATING, READING AND UPDATING TODOS.
        """
    serializer_class = serializers.MultimediaSerializer
    queryset = models.Multimedia.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description_file')

    authentication_classes = (TokenAuthentication,)