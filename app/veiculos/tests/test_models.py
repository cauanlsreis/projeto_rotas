from django.test import TestCase
from app.veiculos.models import veiculos


class TestVeiculosModel(TestCase):
    def test_criacao_veiculo(self):
        veiculo = veiculos.objects.create(
            quantidade_passageiros=4,
            modelo="Gol",
            cor="Branco",
            placa="ABC1234"
        )
        self.assertEqual(veiculo.placa, "ABC1234")
        self.assertEqual(veiculo.modelo, "Gol")
        self.assertTrue(veiculo.ativo)

    def test_coordenadas_opcionais_veiculos(self):
        """Testa se latitude e longitude são opcionais para veículos"""
        veiculo = veiculos.objects.create(
            quantidade_passageiros=4,
            modelo="Gol",
            cor="Branco",
            placa="XYZ5678"
            # latitude e longitude omitidas (devem ser null)
        )
        self.assertIsNone(veiculo.latitude)
        self.assertIsNone(veiculo.longitude)
        self.assertTrue(veiculo.ativo)

    def test_coordenadas_com_valores_veiculos(self):
        """Testa se veículos podem ter coordenadas quando fornecidas"""
        veiculo = veiculos.objects.create(
            quantidade_passageiros=5,
            modelo="Civic",
            cor="Prata",
            placa="DEF9876",
            latitude=-22.906847,
            longitude=-43.172896
        )
        self.assertIsNotNone(veiculo.latitude)
        self.assertIsNotNone(veiculo.longitude)
        self.assertEqual(float(veiculo.latitude), -22.906847)
        self.assertEqual(float(veiculo.longitude), -43.172896)
