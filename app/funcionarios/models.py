from django.db import models
from app.alojamentos.models import Alojamentos
from app.usuarios.models import Usuario
from app.veiculos.models import veiculos
from app.obras.models import Obras

class Funcionarios(models.Model):
    id = models.AutoField(primary_key=True)
    nome_completo = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    alojamento = models.ForeignKey(Alojamentos, on_delete=models.CASCADE)
    obra = models.ForeignKey(Obras, on_delete=models.SET_NULL, null=True, blank=True)
    veiculo = models.ForeignKey(veiculos, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    data_cadastro = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'funcionarios'

    def __str__(self):
        return self.nome_completo
