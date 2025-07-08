from django.test import TestCase
from app.rotas.models import Rota
from app.obras.models import Obras


class TestRotasViews(TestCase):
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
        self.rota = Rota.objects.create(
            descricao_transporte="Transporte Teste",
            obra_destino=self.obra,
            tipo_trecho='IDA',
            ordem_paradas={"paradas": []}
        )

    def test_rota_criada_com_sucesso(self):
        self.assertEqual(self.rota.descricao_transporte, "Transporte Teste")
        self.assertEqual(self.rota.obra_destino, self.obra)
        self.assertEqual(self.rota.tipo_trecho, 'IDA')
