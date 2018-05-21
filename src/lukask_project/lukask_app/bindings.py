from channels_api.bindings import ResourceBinding
from .models import Publication
from .serializers import PublicationSerializer
from channels_api.permissions import IsAuthenticated

class PublicationBinding(ResourceBinding):
    model = Publication
    stream = "publication"
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all()

