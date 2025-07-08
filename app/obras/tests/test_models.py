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

    def test_latitude_longitude_obrigatorios_obras(self):
        """Testa se latitude e longitude são obrigatórios para obras"""
        with self.assertRaises(Exception):
            # Deve falhar pois latitude/longitude são obrigatórios
            Obras.objects.create(
                nome="Obra Sem Coordenadas",
                endereco="Rua da Obra",
                numero="456",
                cidade="Rio de Janeiro",
                estado="RJ"
                # latitude e longitude ausentes
            )

    def test_coordenadas_validas_obras(self):
        """Testa se coordenadas válidas são aceitas para obras"""
        obra = Obras.objects.create(
            nome="Obra Com Coordenadas",
            endereco="Rua da Obra",
            numero="456",
            cidade="Rio de Janeiro",
            estado="RJ",
            latitude=-22.906847,  # Coordenada válida do Rio de Janeiro
            longitude=-43.172896
        )
        self.assertIsNotNone(obra.latitude)
        self.assertIsNotNone(obra.longitude)
        self.assertEqual(float(obra.latitude), -22.906847)
        self.assertEqual(float(obra.longitude), -43.172896)
