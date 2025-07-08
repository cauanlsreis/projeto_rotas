# app/rotas/serializers.py

from rest_framework import serializers
from .models import Rota  # ajuste se o nome do modelo for diferente


class RotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rota
        fields = '__all__'
