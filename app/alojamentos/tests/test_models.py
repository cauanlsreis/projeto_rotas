from django.test import TestCase
from app.alojamentos.models import Alojamentos


class TestAlojamentosModel(TestCase):
    def test_criacao_alojamento(self):
        aloj = Alojamentos.objects.create(
            nome="Teste Alojamento",
            endereco="Rua Teste",
            numero="123",
            cidade="São Paulo",
            estado="SP",
            latitude=-23.550520,
            longitude=-46.633309
        )
        self.assertEqual(aloj.nome, "Teste Alojamento")
        self.assertEqual(aloj.cidade, "São Paulo")
