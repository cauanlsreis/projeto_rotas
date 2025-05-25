from rest_framework import generics 
from .models import Alojamentos
from .serializers import AlojamentosSerializer

class AlojamentosCreateView(generics.CreateAPIView):
    queryset = Alojamentos.objects.all()
    serializer_class = AlojamentosSerializer

class AlojamentosListView(generics.ListAPIView):
    queryset = Alojamentos.objects.all()
    serializer_class = AlojamentosSerializer
