from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Funcionarios
from .serializers import FuncionariosSerializer

class FuncionariosCreateListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Funcionarios.objects.all()
    serializer_class = FuncionariosSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "mensagem": "Funcionário cadastrado com sucesso!",
            "dados": serializer.data
        }, status=status.HTTP_201_CREATED)
    
class FuncionariosListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Funcionarios.objects.all()
    serializer_class = FuncionariosSerializer
