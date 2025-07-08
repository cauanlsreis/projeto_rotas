from django.test import TestCase
from app.usuarios.models import Usuario


class TestUsuariosModel(TestCase):
    def test_criacao_usuario(self):
        usuario = Usuario.objects.create(
            nome="João Silva",
            email="joao@teste.com",
            cpf="12345678901"
        )
        self.assertEqual(usuario.nome, "João Silva")
        self.assertEqual(usuario.email, "joao@teste.com")
        self.assertTrue(usuario.is_active)
