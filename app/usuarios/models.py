from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    senha = models.CharField(max_length=255)
    confirmacao_senha = models.CharField(max_length=255)
    data_cadastro = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'