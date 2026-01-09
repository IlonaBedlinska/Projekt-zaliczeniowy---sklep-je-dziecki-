from rest_framework import generics
from .models import Produkt, Kategoria
from .serializers import ProduktSerializer, KategoriaSerializer


class ProduktListCreateView(generics.ListCreateAPIView):
    queryset = Produkt.objects.all()
    serializer_class = ProduktSerializer


class ProduktDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produkt.objects.all()
    serializer_class = ProduktSerializer


class KategoriaListView(generics.ListCreateAPIView):
    queryset = Kategoria.objects.all()
    serializer_class = KategoriaSerializer

class KategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kategoria.objects.all()
    serializer_class = KategoriaSerializer