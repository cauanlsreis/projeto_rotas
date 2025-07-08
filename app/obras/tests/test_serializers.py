from django.test import TestCase
from app.obras.models import Obras


class TestObrasSerializers(TestCase):
    def test_obra_creation(self):
        obra = Obras.objects.create(
            nome="Nova Obra",
            endereco="Rua Nova",
            numero="789",
            cidade="Belo Horizonte",
            estado="MG",
            latitude=-19.916681,
            longitude=-43.934493
        )
        self.assertEqual(obra.nome, "Nova Obra")
        self.assertEqual(obra.cidade, "Belo Horizonte")
