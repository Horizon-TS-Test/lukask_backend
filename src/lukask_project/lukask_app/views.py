# Create your views here.
from django.http import Http404
from django.http.request import UnreadablePostError
from rest_framework import viewsets,generics
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from . import permissions
from . import serializers
from . import models
from .lukask_constants import LukaskConstants

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, RETRIEVEING, UPDATING AND DELETING PROFILES.
    """

    serializer_class = serializers.UserProfileSerializer
    permission_classes = (permissions.UpdateOwnProfile,)
    queryset = models.UserProfile.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email',)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(is_active = LukaskConstants.LOGICAL_STATE_ACTIVE)

    def get_queryset(self):

        req = self.request
        qr_user_rel_pub = req.query_params.get(LukaskConstants.USERS_RELEVANCE_PUBLICATION)
        qr_user_rel_com = req.query_params.get(LukaskConstants.USERS_RELEVANCE_COMMENT)

        if qr_user_rel_pub is not None:
            return models.UserProfile.objects.filter(actionUserReg__type_action__description_action = LukaskConstants.TYPE_ACTION_RELEVANCE, actionUserReg__publication = qr_user_rel_pub, actionUserReg__active = LukaskConstants.LOGICAL_STATE_ACTIVE, actionUserReg__action_parent = None)
        if qr_user_rel_com is not None:
            print ("qr_user_rel_com ", qr_user_rel_com)
            return models.UserProfile.objects.filter(actionUserReg__type_action__description_action = LukaskConstants.TYPE_ACTION_RELEVANCE, actionUserReg__action_parent__id_action = qr_user_rel_com, actionUserReg__active = LukaskConstants.LOGICAL_STATE_ACTIVE)
        return  models.UserProfile.objects.filter(is_active = LukaskConstants.LOGICAL_STATE_ACTIVE)


class ProvinceViewSet(viewsets.ModelViewSet):
    """
       HANDLES CREATING, READING AND UPDATING PROVINCE.
       """
    serializer_class = serializers.ProvinceSerializer
    queryset = models.Province.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description_province')


class CantonViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, READING AND UPDATING CANTON.
    """
    serializer_class = serializers.CantonSerializer
    queryset = models.Canton.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description_canton')

class ParishViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, READING AND UPDATING TYPEACTION.
    """
    serializer_class = serializers.ParishSerializer
    queryset = models.Parish.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description_parish')


class PersonViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, RETRIEVEING, UPDATING AND DELETING PROFILES.
    """

    serializer_class = serializers.PersonSerializer
    ##permission_classes = (permissions.UdateOwnProfile, IsAuthenticated)
    queryset = models.Person.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('identification_card', 'name', 'last_name',)
    #authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(active = LukaskConstants.LOGICAL_STATE_ACTIVE)


class LoginViewSet(viewsets.ViewSet):
    """
    CHECK email AND password AND RETURNS AN AUTH TOKEN
    """

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """
        USE THE ObtainedAuthToken APIView TO VALIDATE AND CREATE A TOKEN.
        """
        _response = ObtainAuthToken().post(request)
        _useremail = request.data.get('username')

        if _useremail is not None:
            _user  = models.UserProfile.objects.filter(email = _useremail)

        if _user is not None:
            serializer = serializers.UserProfileSerializer(_user, many=True)
            _response.data['user_id'] = serializer.data[0].get("id")
        return _response


    def get_authenticate_header(self, request):
        pass


class TypeActionViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, READING AND UPDATING TYPEACTION.
    """
    serializer_class = serializers.TypeActionSerializer
    queryset = models.TypeAction.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description_action')
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(active = LukaskConstants.LOGICAL_STATE_ACTIVE)



class ActionViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, READING AND UPDATING TODOS.
    """
    serializer_class = serializers.ActionSerializer
    queryset = models.ActionPublication.objects.exclude(active = LukaskConstants.LOGICAL_STATE_INACTIVE).order_by('-date_register')
    search_fields = ('description','publication__id_publication')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('type_action__id_type_action', 'publication__id_publication', 'action_parent__id_action')
    permission_classes = (permissions.UserProfilePublication, IsAuthenticated)
    authentication_classes = (TokenAuthentication,)

    def get_user_register(self, pk):
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        try:
            serializer.save(user_register = self.request.user)
        except UnreadablePostError:
            print (Http404.message)
            raise Http404

    def get_queryset(self):
        """
        Filtros para consultas de acciones sobre la publication
        :return: List
        """
        req = self.request
        qrOp = req.query_params.get('qrOp')
        print ("qrOP", qrOp)
        if qrOp is None:
            return models.ActionPublication.objects.filter(active=LukaskConstants.LOGICAL_STATE_ACTIVE).order_by('-date_register')
        if qrOp == LukaskConstants.FILTERS_ACTION_REPLIES:
            return models.ActionPublication.objects.filter(active=LukaskConstants.LOGICAL_STATE_ACTIVE).exclude(action_parent=None).order_by('-date_register')
        elif qrOp == LukaskConstants.FILTERS_ACTION_COMMENTS:
            return models.ActionPublication.objects.filter(active=LukaskConstants.LOGICAL_STATE_ACTIVE).exclude(~Q(action_parent=None)).order_by('-date_register')

    def get_serializer_context(self):
        return {'user': self.request.user.email}

class PriorityPublicationViewSet(viewsets.ModelViewSet):
    """"
    HANDLES CREATING, READING AND UPDATING TODOS.
        """
    serializer_class = serializers.PriorityPublicationSerializer
    queryset = models.PriorityPublication.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description')

    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user_register = self.request.user, active = LukaskConstants.LOGICAL_STATE_ACTIVE)

class TypePublicationViewSet(viewsets.ModelViewSet):
    """"
    HANDLES CREATING, READING AND UPDATING TODOS.
        """
    serializer_class = serializers.TypePublicationSerializer
    queryset = models.TypePublication.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description',)

    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user_register = self.request.user, active = LukaskConstants.LOGICAL_STATE_ACTIVE)


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
    queryset = models.Publication.objects.exclude(active = LukaskConstants.LOGICAL_STATE_INACTIVE).order_by('-date_publication')
    permission_classes = (permissions.UserProfilePublication, IsAuthenticated)
    parser_classes = (MultiPartParser, FormParser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('detail', 'location')
    authentication_classes = (TokenAuthentication,)

    def get_user_register(self, pk):
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        try :
            serializer.save(user_register = self.request.user, active = LukaskConstants.LOGICAL_STATE_ACTIVE)
        except UnreadablePostError:
            print (Http404.message)
            raise Http404

    def perform_update(self, serializer):
        try:
            serializer.save(user_update = self.request.user)
        except UnreadablePostError:
            raise Http404

    def get_serializer_context(self):
        return {'user': self.request.user.email}

class MultimediaViewSet(viewsets.ModelViewSet):
    """"
    HANDLES CREATING, READING AND UPDATING TODOS.
    """
    serializer_class = serializers.MultimediaSerializer
    queryset = models.Multimedia.objects.exclude(active = LukaskConstants.LOGICAL_STATE_INACTIVE)
    filter_backends = (filters.SearchFilter,)
    parser_classes = (MultiPartParser, FormParser,)
    search_fields = ('description_file')
    permission_classes = (permissions.UserProfilePublication, IsAuthenticated)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        """
        Creacion de medios
        :param serializer:
        :return:
        """
        serializer.save(user_register = self.request.user, active = LukaskConstants.LOGICAL_STATE_ACTIVE)

    def perform_update(self, serializer):
        """
        Actualizacion de medios
        :param serializer:
        :return:
        """
        serializer.save(user_update = self.request.user)

    def get_user_register(self, pk):
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404


class MultimediaSingleAPIView(generics.ListCreateAPIView):
    """
    view para gestion de imagenes
    """
    serializer_class = serializers.MultimediaSingleSerializer
    queryset = models.Multimedia.objects.exclude(active = LukaskConstants.LOGICAL_STATE_INACTIVE)
    filter_backends = (filters.SearchFilter,)
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (permissions.UserProfilePublication, IsAuthenticated)
    search_fields = ('id_multimedia')
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        print("serializers", serializer)
        serializer.save(user_register = self.request.user, active = LukaskConstants.LOGICAL_STATE_ACTIVE)

    def get_user_register(self, pk):
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404

class NotificationViewSet(viewsets.ModelViewSet):
    """
    View para gestionar Notificaciones
    """
    serializer_class =  serializers.NotificationSerializer
    queryset = models.Notification.objects.exclude(active = LukaskConstants.LOGICAL_STATE_INACTIVE).order_by('-date_register')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('date_generated_notification')
    permission_classes = (permissions.UserProfilePublication, IsAuthenticated)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user_register = self.request.user, active = LukaskConstants.LOGICAL_STATE_ACTIVE)


    def get_user_register(self, pk):
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404


class NotificationReceivedViewSet(viewsets.ModelViewSet):
    """
    View para gestionar Notificaciones
    """
    serializer_class =  serializers.NotificationReceivedSerializer
    queryset = models.NotificationReceived.objects.exclude(active = LukaskConstants.LOGICAL_STATE_INACTIVE).order_by('-date_register')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user_received',)
    search_fields = ('notification')

    def get_user_register(self, pk):
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404

