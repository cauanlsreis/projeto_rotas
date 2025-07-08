from django.test import TestCase
from app.funcionarios.models import Funcionarios
from app.alojamentos.models import Alojamentos


class TestFuncionariosSerializers(TestCase):
    def setUp(self):
        self.alojamento = Alojamentos.objects.create(
            nome="Alojamento Teste",
            endereco="Rua Teste",
            numero="123",
            cidade="São Paulo",
            estado="SP",
            latitude=-23.550520,
            longitude=-46.633309
        )

    def test_funcionario_creation(self):
        funcionario = Funcionarios.objects.create(
            nome_completo="Maria Silva",
            cpf="987.654.321-00",
            alojamento=self.alojamento
        )
        self.assertEqual(funcionario.nome_completo, "Maria Silva")
