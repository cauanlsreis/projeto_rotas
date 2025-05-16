from rest_framework import serializers
from .models import Obras

class ObrasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obras
        fields = '__all__'
        extra_kwargs = {
            'estado': {
                'error_messages': {
                    'max_length': 'O campo estado deve conter no máximo 2 caracteres.',
                    'blank': 'O campo estado é obrigatório.',
                }
            },
            'nome': {
                'error_messages': {
                    'blank': 'O campo nome é obrigatório.',
                }
            },
            'cidade': {
                'error_messages': {
                    'blank': 'O campo cidade é obrigatório.',
                }
            },
             'numero': {
                'error_messages': {
                    'blank': 'O campo numero é obrigatório.',
                }
            },
             'endereco': {
                'error_messages': {
                    'blank': 'O campo endereço é obrigatório.',
                }
            },
             'latitude': {
                'error_messages': {
                    'blank': 'O campo latitude é obrigatório.',
                }
            },
             'longitude': {
                'error_messages': {
                    'blank': 'O campo longitude é obrigatório.',
                }
            },
        }

    def validate_estado(self, value):
        if len(value.strip()) != 2:
            raise serializers.ValidationError("O campo estado deve conter exatamente 2 letras.")
        return value.upper()

    def validate_latitude(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("A latitude deve estar entre -90 e 90.")
        return value

    def validate_longitude(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("A longitude deve estar entre -180 e 180.")
        return value

    def validate(self, data):
        campos_obrigatorios = ['nome', 'endereco', 'numero', 'cidade', 'estado', 'latitude', 'longitude']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                raise serializers.ValidationError({campo: f"O campo {campo} é obrigatório."})

        if not self.instance:
            if Obras.objects.filter(
                endereco=data['endereco'],
                numero=data['numero'],
                cidade=data['cidade'],
                estado=data['estado'],
                latitude=data['latitude'],
                longitude=data['longitude']
            ).exists():
                raise serializers.ValidationError({"endereco": "Endereço já cadastrado com essa localização."})

        return data
