from rest_framework import serializers
from .models import Funcionarios
from app.alojamentos.models import Alojamentos
from django.db.models import Count, F


class AlojamentoInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alojamentos
        fields = ['id', 'nome', 'endereco', 'numero',
                  'cidade', 'estado', 'latitude', 'longitude']


class FuncionariosSerializer(serializers.ModelSerializer):

    alojamento = serializers.PrimaryKeyRelatedField(
        queryset=Alojamentos.objects.annotate(
            # Cria um campo temporário 'num_funcionarios' em cada alojamento
            num_funcionarios=Count('funcionarios') 
        ).filter(
            # Filtra para incluir apenas onde a contagem é MENOR que a capacidade
            num_funcionarios__lt=F('quantidade_de_vagas')
        ),
        # Adiciona a mensagem de erro para quando o campo é obrigatório
        required=True,
        allow_null=False,
        error_messages={
            'required': 'O campo alojamento é obrigatório.',
            'does_not_exist': 'Alojamento inválido ou sem vagas disponíveis.',
            'incorrect_type': 'Tipo incorreto. O valor esperado é um ID de alojamento.'
        }
    )

    class Meta:
        model = Funcionarios
        fields = ['id', 'nome_completo', 'cpf', 'alojamento',
                  'obra', 'data_cadastro']

    def validate(self, data):
        if not self.instance:
            # Criação: nome_completo e cpf obrigatórios
            campos = ['nome_completo', 'cpf']
            for campo in campos:
                if not data.get(campo):
                    raise serializers.ValidationError(
                        {campo: f"O campo '{campo}' é obrigatório."})
        else:
            # Atualização: apenas cpf obrigatório
            if 'cpf' not in data or not data.get('cpf'):
                raise serializers.ValidationError(
                    {"cpf": "O campo 'cpf' é obrigatório."})

        cpf = data.get('cpf')
        if cpf:
            if not cpf.isdigit() or len(cpf) != 11:
                raise serializers.ValidationError(
                    {"cpf": "O CPF deve conter apenas números e ter 11 dígitos."})
            # Se for criação ou alteração do CPF, verifica duplicidade
            if not self.instance or (self.instance and cpf != self.instance.cpf):
                if Funcionarios.objects.filter(cpf=cpf).exists():
                    raise serializers.ValidationError(
                        {"cpf": "CPF já cadastrado no sistema."})

        return data

    def create(self, validated_data):
        funcionario = Funcionarios.objects.create(**validated_data)
        return funcionario
