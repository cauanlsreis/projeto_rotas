from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated
from .models import Alojamentos
from .serializers import AlojamentosSerializer

class AlojamentosCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Alojamentos.objects.all()
    serializer_class = AlojamentosSerializer

class AlojamentosListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Alojamentos.objects.all()
    serializer_class = AlojamentosSerializer
