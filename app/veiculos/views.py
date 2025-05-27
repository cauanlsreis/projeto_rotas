from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import veiculos
from .serializers import VeiculoSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except AuthenticationFailed:
            raise AuthenticationFailed("Você não inseriu corretamente as credenciais de autenticação")

class VeiculoCreateListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
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
