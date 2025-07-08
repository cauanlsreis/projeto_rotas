from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from app.alojamentos.models import Alojamentos


# Usando TestCase simples ao invés de APITestCase
class TestAlojamentosViews(TestCase):
    def setUp(self):
        self.alojamento = Alojamentos.objects.create(
            nome="Alojamento Teste",
            endereco="Rua Teste",
            numero="123",
            cidade="São Paulo",
            estado="SP",
            latitude=-23.550520,
            longitude=-46.633309
        )

    def test_alojamento_criado_com_sucesso(self):
        # Teste simples para verificar se o alojamento foi criado
        self.assertEqual(self.alojamento.nome, "Alojamento Teste")
        self.assertEqual(self.alojamento.cidade, "São Paulo")

    def test_str_method(self):
        # Teste do método __str__ do modelo
        expected = "Alojamento Teste - São Paulo/SP"
        self.assertEqual(str(self.alojamento), expected)
