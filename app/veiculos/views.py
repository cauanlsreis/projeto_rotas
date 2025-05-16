from rest_framework import generics, status
from rest_framework.response import Response
from .models import veiculos
from .serializers import VeiculoSerializer

class VeiculoCreateListView(generics.ListCreateAPIView):
    queryset = veiculos.objects.all()
    serializer_class = VeiculoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "mensagem": "Veículo cadastrado com sucesso!",
            "dados": serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)
