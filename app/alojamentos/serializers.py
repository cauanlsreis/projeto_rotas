from rest_framework import serializers
from .models import Alojamentos

class AlojamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alojamentos
        fields = '__all__'

    def validate_estado(self, value):
        if len(value) != 2:
            raise serializers.ValidationError("O campo estado deve conter exatamente 2 letras.")
        return value.upper()

    def validate_latitude(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("Latitude deve estar entre -90 e 90")
        return value

    def validate_longitude(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("Longitude deve estar entre -180 e 180")
        return value

    def validate(self, data):
        obrigatorio = ['nome', 'estado', 'cidade', 'latitude', 'longitude', 'numero', 'endereco']
        for campo in obrigatorio:
            if not data.get(campo):
                raise serializers.ValidationError(f"O campo '{campo}' é obrigatório.")
        return data
