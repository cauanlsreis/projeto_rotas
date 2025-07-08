from django.test import TestCase
from app.veiculos.models import veiculos


class TestVeiculosSerializers(TestCase):
    def test_veiculo_creation(self):
        veiculo = veiculos.objects.create(
            quantidade_passageiros=5,
            modelo="Civic",
            cor="Prata",
            placa="XYZ9876"
        )
        self.assertEqual(veiculo.modelo, "Civic")
        self.assertEqual(veiculo.placa, "XYZ9876")
        self.assertTrue(veiculo.ativo)
