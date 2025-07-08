from django.test import TestCase
from app.rotas.models import Rota
from app.obras.models import Obras


class TestRotasSerializers(TestCase):
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

    def test_rota_creation(self):
        rota = Rota.objects.create(
            descricao_transporte="Nova Rota",
            obra_destino=self.obra,
            tipo_trecho='VOLTA',
            ordem_paradas={"paradas": ["local1", "local2"]}
        )
        self.assertEqual(rota.descricao_transporte, "Nova Rota")
        self.assertEqual(rota.tipo_trecho, "VOLTA")
