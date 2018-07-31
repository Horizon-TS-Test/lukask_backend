from channels_api.bindings import ResourceBinding

from .models import Multimedia
from .models import Publication
from .models import ActionPublication
from .models import NotificationReceived
from .serializers import PublicationSerializer
from .serializers import MultimediaSerializer
from .serializers import ActionSerializer
from .serializers import NotificationReceivedSerializer
from channels_api.permissions import IsAuthenticated

class PublicationBinding(ResourceBinding):
    model = Publication
    stream = "publication"
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all()


class MultimediaBinding(ResourceBinding):
    model = Multimedia
    stream = "multimedia"
    serializer_class = MultimediaSerializer
    queryset = Multimedia.objects.all()

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