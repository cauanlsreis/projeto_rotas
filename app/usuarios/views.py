from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuarioSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated

# Create your views here.

def home(request):
    return render(request,'usuarios/home.html')


class CadastroUsuarioAPIView(APIView):
    permission_classes = []  # Permitir acesso público para cadastro
    
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            refresh = RefreshToken.for_user(usuario)
            return Response({
                'mensagem': 'Usuário cadastrado com sucesso!',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []  
    
    def post(self, request):
        email = request.data.get('email')
        senha = request.data.get('senha')
        from .models import Usuario
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.check_password(senha):
                refresh = RefreshToken.for_user(usuario)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
            else:
                raise Usuario.DoesNotExist
        except Usuario.DoesNotExist:
            return Response(
                {'detail': 'Usuário ou senha inválidos.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class UsuarioMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)