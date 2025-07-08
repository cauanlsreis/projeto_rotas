from django.test import TestCase
from app.funcionarios.models import Funcionarios
from app.alojamentos.models import Alojamentos


class TestFuncionariosModel(TestCase):
    def test_criacao_funcionario(self):
        # Primeiro criar um alojamento (necessário para o funcionário)
        alojamento = Alojamentos.objects.create(
            nome="Alojamento Teste",
            endereco="Rua Teste",
            numero="123",
            cidade="São Paulo",
            estado="SP",
            latitude=-23.550520,
            longitude=-46.633309
        )

        funcionario = Funcionarios.objects.create(
            nome_completo="João Silva",
            cpf="123.456.789-00",
            alojamento=alojamento
        )
        self.assertEqual(funcionario.nome_completo, "João Silva")
        self.assertEqual(funcionario.cpf, "123.456.789-00")
