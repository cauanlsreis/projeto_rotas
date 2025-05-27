from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .usermanager import UsuarioManager

class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    senha = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)  # senha já existe, mas para compatibilidade com AbstractBaseUser:
    data_cadastro = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf', 'nome']

    objects = UsuarioManager()

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.senha = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.senha)