from django.db import models
from app.obras.models import Obras

class veiculos(models.Model):
    id = models.AutoField(primary_key=True)
    quantidade_passageiros = models.PositiveIntegerField()
    modelo = models.CharField(max_length=100)
    cor = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True)
    data_cadastro = models.DateField(auto_now_add=True)
    obra_id = models.ForeignKey(Obras, on_delete=models.SET_NULL, null=True, blank=True, related_name='veiculos')

    class Meta:
        db_table = 'veiculos'

    def __str__(self):
        return f"{self.modelo} - {self.placa}"
