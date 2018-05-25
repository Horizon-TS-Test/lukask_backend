from channels_api.bindings import ResourceBinding

from .models import Multimedia
from .models import Publication
from .serializers import PublicationSerializer
from .serializers import MultimediaSerializer
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


