from django.test import TestCase
from app.obras.models import Obras


class TestObrasModel(TestCase):
    def test_criacao_obra(self):
        obra = Obras.objects.create(
            nome="Teste Obra",
            endereco="Rua da Obra",
            numero="456",
            cidade="Rio de Janeiro",
            estado="RJ",
            latitude=-22.906847,
            longitude=-43.172896
        )
        self.assertEqual(obra.nome, "Teste Obra")
        self.assertEqual(obra.cidade, "Rio de Janeiro")
