from rest_framework import serializers
from .models import Alojamentos

class AlojamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alojamentos
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
            'quantidade_de_vagas': {
                'error_messages': {
                    'required': 'O campo quantidade de vagas é obrigatório.',
                    'invalid': 'A quantidade de vagas deve ser um número inteiro válido.'
                }
            }
        }

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
    def validate_quantidade_de_vagas(self, value):
        if value > 100: # Exemplo: um alojamento não pode ter mais que 500 vagas
            raise serializers.ValidationError("A quantidade de vagas não pode ser maior que 500.")
        return value

    def validate(self, data):
        # Se for criação (self.instance é None)
        if not self.instance:
            obrigatorio = ['nome', 'estado', 'cidade', 'latitude', 'longitude', 'numero', 'endereco','quantidade_de_vagas']
            for campo in obrigatorio:
                if not data.get(campo):
                    raise serializers.ValidationError({campo: f"O campo {campo} é obrigatório."})
            if Alojamentos.objects.filter(
                endereco=data['endereco'],
                numero=data['numero'],
                cidade=data['cidade'],
                estado=data['estado'],
                latitude=data['latitude'],
                longitude=data['longitude']
            ).exists():
                raise serializers.ValidationError({"endereco": "Alojamentos ja cadastrado com esse endereço."})
        else:
            # Atualização: só o nome é obrigatório
            if 'nome' not in data or not data.get('nome'):
                raise serializers.ValidationError({'nome': "O campo nome é obrigatório."})
        return data
