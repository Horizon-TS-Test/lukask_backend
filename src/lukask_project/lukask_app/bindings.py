
from channels_api.bindings import ResourceBinding
from channels_api.decorators import detail_action, list_action

#from .models import Multimedia
from .models import Publication
from .models import ActionPublication
from .models import NotificationReceived
from .serializers import PublicationSerializer
#from .serializers import MultimediaSerializer
from .serializers import ActionSerializer
from .serializers import NotificationReceivedSerializer

class PublicationBinding(ResourceBinding):
    model = Publication
    stream = "publication"
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all()

    @detail_action()
    def custom_create(self, pk, data=None, **kwargs):
        publication = Publication.objects.get(id_publication = pk)
        serializer_p = PublicationSerializer(publication)
        result =  serializer_p.data
        return result, 200
    
    @detail_action()
    def custom_update(self, pk, data=None, **kwargs):
        publication = Publication.objects.get(id_publication = pk)
        serializer_p = PublicationSerializer(publication)
        result =  serializer_p.data
        return result, 200

    """@list_action()
    def report(self, data=None, **kwargs):
        report = self.get_queryset()
        return report, 200"""


"""class MultimediaBinding(ResourceBinding):
    model = Multimedia
    stream = "multimedia"
    serializer_class = MultimediaSerializer
    queryset = Multimedia.objects.all()"""

class ActionPublicationBinding(ResourceBinding):
    model = ActionPublication
    stream = "actions"
    serializer_class = ActionSerializer
    queryset = ActionPublication.objects.all()

class NotificationReceivedBinding(ResourceBinding):
    model = NotificationReceived
    stream = "notification_received"
    serializer_class = NotificationReceivedSerializer
    queryset = NotificationReceived.objects.all()