from rest_framework import generics 
from .models import Alojamentos
from .serializers import AlojamentosSerializer

class AlojamentosListCreateView(generics.ListCreateAPIView):
    queryset = Alojamentos.objects.all()
    serializer_class = AlojamentosSerializer

