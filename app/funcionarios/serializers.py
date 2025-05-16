from rest_framework import serializers
from .models import Funcionarios
from app.alojamentos.models import Alojamentos

class AlojamentoInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alojamentos
        fields = ['id', 'nome', 'endereco', 'numero', 'cidade', 'estado', 'latitude', 'longitude']

class FuncionariosSerializer(serializers.ModelSerializer):
    novo_alojamento = AlojamentoInlineSerializer(write_only=True, required=False)

    class Meta:
        model = Funcionarios
        fields = ['id', 'nome_completo', 'cpf', 'alojamento', 'novo_alojamento', 'obra', 'veiculo', 'usuario', 'data_cadastro']

    def validate(self, data):
        campos = ['nome_completo', 'cpf']
        for campo in campos:
            if not data.get(campo):
                raise serializers.ValidationError({campo: f"O campo '{campo}' é obrigatório."})

        cpf = data.get('cpf')
        if not cpf.isdigit() or len(cpf) != 11:
            raise serializers.ValidationError({"cpf": "O CPF deve conter apenas números e ter 11 dígitos."})

        if Funcionarios.objects.filter(cpf=cpf).exists():
            raise serializers.ValidationError({"cpf": "CPF já cadastrado no sistema."})

        return data

    def create(self, validated_data):
        novo_alojamento_data = validated_data.pop('novo_alojamento', None)

        if novo_alojamento_data:
            alojamento = Alojamentos.objects.create(**novo_alojamento_data)
        else:
            alojamento = validated_data.get('alojamento')

        funcionario = Funcionarios.objects.create(
            nome_completo=validated_data['nome_completo'],
            cpf=validated_data['cpf'],
            alojamento=alojamento,
            obra=validated_data.get('obra'),
            veiculo=validated_data.get('veiculo'),
            usuario=validated_data.get('usuario')
        )

        return funcionario
