from django.test import TestCase
from app.rotas.models import Rota
from app.obras.models import Obras


class TestRotasModel(TestCase):
    def test_criacao_rota(self):
        # Primeiro criar uma obra (necessária para a rota)
        obra = Obras.objects.create(
            nome="Obra Teste",
            endereco="Rua da Obra",
            numero="456",
            cidade="Rio de Janeiro",
            estado="RJ",
            latitude=-22.906847,
            longitude=-43.172896
        )

        rota = Rota.objects.create(
            descricao_transporte="Transporte Teste",
            obra_destino=obra,
            tipo_trecho='IDA',
            ordem_paradas={"paradas": []}
        )
        self.assertEqual(rota.descricao_transporte, "Transporte Teste")
        self.assertEqual(rota.tipo_trecho, "IDA")
