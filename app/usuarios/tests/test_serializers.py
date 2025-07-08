from django.test import TestCase
from app.usuarios.models import Usuario


class TestUsuariosSerializers(TestCase):
    def test_usuario_creation(self):
        usuario = Usuario.objects.create(
            nome="Maria Santos",
            email="maria@teste.com",
            cpf="98765432109"
        )
        self.assertEqual(usuario.nome, "Maria Santos")
        self.assertEqual(usuario.email, "maria@teste.com")
        self.assertTrue(usuario.is_active)
