from rest_framework import serializers
from .models import veiculos
import re


class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = veiculos
        fields = '__all__'
        extra_kwargs = {
            'quantidade_passageiros': {
                'error_messages': {
                    'required': 'O campo quantidade_passageiros é obrigatório.',
                    'invalid': 'Quantidade de passageiros deve ser um número positivo.'
                }
            },
            'modelo': {'error_messages': {'blank': 'O campo modelo é obrigatório.'}},
            'cor': {'error_messages': {'blank': 'O campo cor é obrigatório.'}},
            'placa': {'error_messages': {'blank': 'O campo placa é obrigatório.'}},
        }

    def validate(self, data):
        if not self.instance:
            # Criação: todos obrigatórios
            obrigatorios = ['quantidade_passageiros', 'modelo', 'cor', 'placa']
            for campo in obrigatorios:
                if not data.get(campo):
                    raise serializers.ValidationError(
                        {campo: f"O campo {campo} é obrigatório."})

            if veiculos.objects.filter(placa=data['placa']).exists():
                raise serializers.ValidationError(
                    {'placa': 'Placa já cadastrada.'})
        else:
            # Atualização: só a placa é obrigatória
            if 'placa' not in data or not data.get('placa'):
                raise serializers.ValidationError(
                    {'placa': "O campo placa é obrigatório."})
            # Se a placa foi alterada, verifica duplicidade
            if 'placa' in data and data['placa'] != self.instance.placa:
                if veiculos.objects.filter(placa=data['placa']).exists():
                    raise serializers.ValidationError(
                        {'placa': 'Placa já cadastrada.'})
        return data

    def validate_placa(self, value):
        padrao = r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$'
        if not re.match(padrao, value.upper()):
            raise serializers.ValidationError(
                "Formato de placa inválido. Use o padrão ABC1D23.")
        return value.upper()

    def validate_quantidade_passageiros(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantidade de passageiros deve ser um número positivo.")
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
