from django.test import TestCase
from app.obras.models import Obras


class TestObrasViews(TestCase):
    def setUp(self):
        self.obra = Obras.objects.create(
            nome="Obra Teste",
            endereco="Rua da Obra",
            numero="456",
            cidade="Rio de Janeiro",
            estado="RJ",
            latitude=-22.906847,
            longitude=-43.172896
        )

    def test_obra_criada_com_sucesso(self):
        self.assertEqual(self.obra.nome, "Obra Teste")
        self.assertEqual(self.obra.cidade, "Rio de Janeiro")

    def test_str_method(self):
        expected = "Obra Teste - Rio de Janeiro/RJ"
        self.assertEqual(str(self.obra), expected)
