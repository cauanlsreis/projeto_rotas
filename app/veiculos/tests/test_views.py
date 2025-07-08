from django.test import TestCase
from app.veiculos.models import veiculos


class TestVeiculosViews(TestCase):
    def setUp(self):
        self.veiculo = veiculos.objects.create(
            quantidade_passageiros=4,
            modelo="Gol",
            cor="Branco",
            placa="ABC1234"
        )

    def test_veiculo_criado_com_sucesso(self):
        self.assertEqual(self.veiculo.modelo, "Gol")
        self.assertEqual(self.veiculo.placa, "ABC1234")
        self.assertTrue(self.veiculo.ativo)

    def test_placa_unique(self):
        # Testa se a placa é única
        with self.assertRaises(Exception):
            veiculos.objects.create(
                quantidade_passageiros=5,
                modelo="Civic",
                cor="Prata",
                placa="ABC1234"  # Placa já existe
            )
