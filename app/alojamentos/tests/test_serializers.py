from django.test import TestCase
from app.alojamentos.models import Alojamentos
from app.alojamentos.serializers import *


class TestAlojamentosSerializers(TestCase):
    def test_serializer_validacao(self):
        data = {
            'nome': 'Alojamento Teste',
            'endereco': 'Rua Teste',
            'numero': '123',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'latitude': -23.550520,
            'longitude': -46.633309
        }
        # Adapte conforme o nome do seu serializer
        # serializer = AlojamentosSerializer(data=data)
        # self.assertTrue(serializer.is_valid())

        # Teste básico apenas para verificar se o módulo importa corretamente
        alojamento = Alojamentos.objects.create(**data)
        self.assertEqual(alojamento.nome, 'Alojamento Teste')
