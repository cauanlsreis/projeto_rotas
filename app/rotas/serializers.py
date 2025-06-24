# app/rotas/serializers.py

from rest_framework import serializers
from .models import Rota

class RotaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Rota.
    """
    class Meta:
        # '__all__' inclui todos os campos do seu modelo Rota na resposta da API.
        # Isso inclui os novos campos que sugerimos (distancia, duracao, etc.)
        fields = '__all__'