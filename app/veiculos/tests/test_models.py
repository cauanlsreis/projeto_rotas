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
