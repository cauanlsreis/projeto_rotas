from rest_framework import serializers
from .models import Usuario
import re
from django.contrib.auth.hashers import make_password


class UsuarioSerializer(serializers.ModelSerializer):
    confirmacao_senha = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['cpf', 'email', 'nome', 'senha', 'confirmacao_senha']
        extra_kwargs = {'senha': {'write_only': True}}

    def validate(self, data):
        if data['senha'] != data['confirmacao_senha']:
            raise serializers.ValidationError({"senha": "As senhas não coincidem."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirmacao_senha')
        validated_data['senha'] = make_password(validated_data['senha'])
        return Usuario.objects.create(**validated_data)
    
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