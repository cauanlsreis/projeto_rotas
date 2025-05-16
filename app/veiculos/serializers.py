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
        obrigatorios = ['quantidade_passageiros', 'modelo', 'cor', 'placa']
        for campo in obrigatorios:
            if not data.get(campo):
                raise serializers.ValidationError({campo: f"O campo {campo} é obrigatório."})

        if veiculos.objects.filter(placa=data['placa']).exists():
            raise serializers.ValidationError({'placa': 'Placa já cadastrada.'})

        return data

    def validate_placa(self, value):
        padrao = r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$'
        if not re.match(padrao, value.upper()):
            raise serializers.ValidationError("Formato de placa inválido. Use o padrão ABC1D23.")
        return value.upper()

    def validate_quantidade_passageiros(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantidade de passageiros deve ser um número positivo.")
        return value
