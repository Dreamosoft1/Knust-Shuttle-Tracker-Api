from rest_framework import generics
from .models import Bus
from .serializers import BusSerializer

class BusListAPIView(generics.ListAPIView):
    queryset = Bus.objects.filter(available=True)
    serializer_class = BusSerializer
