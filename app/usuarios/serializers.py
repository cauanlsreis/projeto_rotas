from rest_framework import serializers
from .models import Usuario
import re
from django.contrib.auth.hashers import make_password


class UsuarioSerializer(serializers.ModelSerializer):
    confirmacao_senha = serializers.CharField(write_only=True, required=True)
    senha = serializers.CharField(write_only=True, required=True)
    cpf =  serializers.CharField(write_only=True, required=True)
    email =  serializers.CharField(write_only=True, required=True)
    nome =  serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ['cpf', 'email', 'nome', 'senha', 'confirmacao_senha']
        extra_kwargs = {'senha': {'write_only': True}}

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
            raise serializers.ValidationError({"senha": ["As senhas não coincidem."]})

        return data

    def create(self, validated_data):
        validated_data.pop('confirmacao_senha')
        # Usa o método set_password do modelo customizado
        usuario = Usuario(
            email=validated_data['email'],
            cpf=validated_data['cpf'],
            nome=validated_data['nome']
        )
        usuario.set_password(validated_data['senha'])
        usuario.save()
        return usuario
    
    def validate_senha(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("A senha deve ter pelo menos 6 caracteres.")
        if len(value) > 20:
            raise serializers.ValidationError("A senha deve ter no máximo 20 caracteres.")
        return value

    def validate_cpf(self, value):
        if not re.match(r'^\d{11}$', value):
            raise serializers.ValidationError("O CPF deve conter exatamente 11 dígitos numéricos.")
        return value

class UsuarioDetalheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['email', 'nome']