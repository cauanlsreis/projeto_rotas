from django.test import TestCase
from app.usuarios.models import Usuario


class TestUsuariosViews(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nome="João Silva",
            email="joao@teste.com",
            cpf="12345678901"
        )

    def test_usuario_criado_com_sucesso(self):
        self.assertEqual(self.usuario.nome, "João Silva")
        self.assertEqual(self.usuario.email, "joao@teste.com")
        self.assertTrue(self.usuario.is_active)

    def test_usuario_email_unique(self):
        # Testa se o email é único
        with self.assertRaises(Exception):
            Usuario.objects.create(
                nome="Outro João",
                email="joao@teste.com",  # Email já existe
                cpf="98765432100"
            )
