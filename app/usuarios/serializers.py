from rest_framework import serializers
from .models import Usuario
import re
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
import logging # Importe a biblioteca de logging



logger = logging.getLogger('logs')


class UsuarioSerializer(serializers.ModelSerializer):
    confirmacao_senha = serializers.CharField(write_only=True, required=True)

        # Sobrescrevemos os campos 'email' e 'cpf' para adicionar validações customizadas
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=Usuario.objects.all(),
                message="Já existe um usuário cadastrado com este e-mail."
            )
        ]
    )
    cpf = serializers.CharField(
        required=True,
        # Validador para garantir que o CPF é único e customizar a mensagem de erro
        validators=[
            UniqueValidator(
                queryset=Usuario.objects.all(),
                message="Já existe um usuário cadastrado com este CPF."
            )
        ]
    )


    class Meta:
        model = Usuario
        fields = ['id', 'cpf', 'email', 'nome', 'senha', 'confirmacao_senha']
        # Adicionei o 'id' aos fields para que ele seja retornado após o cadastro.
        extra_kwargs = {
            'senha': {'write_only': True},
            'cpf': {'write_only': True},
            'email': {'write_only': True},
            'nome': {'write_only': True},
        }

    def validate(self, data):
        
        obrigatorio = ['nome', 'email', 'cpf', 'senha', 'confirmacao_senha']
        erros = {}

        for campo in obrigatorio:
            if not data.get(campo):
                erros[campo] = [f"O campo '{campo}' é obrigatório."]

        if erros:
            raise serializers.ValidationError(erros)

        # Validação senhas iguais
        if data['senha'] != data['confirmacao_senha']:
            erro_msg = "As senhas não coincidem."
            # Registra o erro no log
            logger.warning(f"Tentativa de cadastro com senhas divergentes para o email: {data.get('email')}")
            raise serializers.ValidationError({"senha": [erro_msg]})

        return data
    
    def validate_email(self, value):
        """
        Verifica se já existe um usuário com o mesmo e-mail.
        """
        if Usuario.objects.filter(email__iexact=value).exists():
            # Registra o erro no log antes de lançar a exceção
            logger.error(f"Tentativa de cadastro com e-mail duplicado: {value}")
            raise serializers.ValidationError("Já existe um usuário cadastrado com este e-mail.")
        return value
    def validate_cpf(self, value):
        """
        Verifica se já existe um usuário com o mesmo CPF e valida o formato.
        """
        if not re.match(r'^\d{11}$', value):
            raise serializers.ValidationError("O CPF deve conter exatamente 11 dígitos numéricos.")
        
        if Usuario.objects.filter(cpf=value).exists():
            # Registra o erro no log antes de lançar a exceção
            logger.error(f"Tentativa de cadastro com CPF duplicado: {value}")
            raise serializers.ValidationError("Já existe um usuário cadastrado com este CPF.")
        return value
        
    def create(self, validated_data):
        validated_data.pop('confirmacao_senha')
        
        # O hashing da senha já é feito pelo método set_password
        usuario = Usuario.objects.create_user(**validated_data)
        
        # Log de sucesso
        logger.info(f"Usuário cadastrado com sucesso - Email: {usuario.email}, CPF: {usuario.cpf}")
        
        return usuario
    
    def validate_senha(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("A senha deve ter pelo menos 6 caracteres.")
        if len(value) > 20:
            raise serializers.ValidationError("A senha deve ter no máximo 20 caracteres.")
        return value


class UsuarioDetalheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['email', 'nome']