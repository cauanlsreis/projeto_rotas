from django.test import TestCase
from app.funcionarios.models import Funcionarios
from app.alojamentos.models import Alojamentos


class TestFuncionariosViews(TestCase):
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
        self.funcionario = Funcionarios.objects.create(
            nome_completo="João Silva",
            cpf="123.456.789-00",
            alojamento=self.alojamento
        )

    def test_funcionario_criado_com_sucesso(self):
        self.assertEqual(self.funcionario.nome_completo, "João Silva")
        self.assertEqual(self.funcionario.alojamento, self.alojamento)

    def test_str_method(self):
        self.assertEqual(str(self.funcionario), "João Silva")
