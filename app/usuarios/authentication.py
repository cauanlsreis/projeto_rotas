from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from django.conf import settings

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except Exception as e:
            return None

    def get_user(self, validated_token):
        try:
            from .models import Usuario
            user_id = validated_token['user_id']
            user = Usuario.objects.filter(id=user_id).first()
            
            if user is None:
                raise exceptions.AuthenticationFailed('Usuário não encontrado.')
            return user
        except Exception as e:
            raise exceptions.AuthenticationFailed('Token inválido')
