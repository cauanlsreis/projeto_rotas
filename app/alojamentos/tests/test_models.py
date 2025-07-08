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

    def test_latitude_longitude_obrigatorios(self):
        """Testa se latitude e longitude são obrigatórios para alojamentos"""
        with self.assertRaises(Exception):
            # Deve falhar pois latitude/longitude são obrigatórios
            Alojamentos.objects.create(
                nome="Alojamento Sem Coordenadas",
                endereco="Rua Teste",
                numero="123",
                cidade="São Paulo",
                estado="SP"
                # latitude e longitude ausentes
            )

    def test_coordenadas_validas(self):
        """Testa se coordenadas válidas são aceitas"""
        aloj = Alojamentos.objects.create(
            nome="Alojamento Coordenadas",
            endereco="Rua Teste",
            numero="123",
            cidade="São Paulo",
            estado="SP",
            latitude=-23.550520,  # Coordenada válida de São Paulo
            longitude=-46.633309
        )
        self.assertIsNotNone(aloj.latitude)
        self.assertIsNotNone(aloj.longitude)
        self.assertEqual(float(aloj.latitude), -23.550520)
        self.assertEqual(float(aloj.longitude), -46.633309)
