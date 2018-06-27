from channels_api.bindings import ResourceBinding

from .models import Multimedia
from .models import Publication
from .models import ActionPublication
from .models import Notification
from .serializers import PublicationSerializer
from .serializers import MultimediaSerializer
from .serializers import ActionSerializer
from .serializers import NotificationSerializer
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
    stream = "comments"
    serializer_class = ActionSerializer
    queryset = ActionPublication.objects.all()

class NotificationBinding(ResourceBinding):
    model = Notification
    stream = "notification"
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()