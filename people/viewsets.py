from rest_framework import viewsets
from people import models
from people import serializers


class PersonTagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PersonTag to be viewed or edited.
    """
    queryset = models.PersonTag.objects.all()
    serializer_class = serializers.PersonTagSerializer
