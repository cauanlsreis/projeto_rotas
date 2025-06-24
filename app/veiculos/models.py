from django.db import models
from app.obras.models import Obras

class veiculos(models.Model):
    id = models.AutoField(primary_key=True)
    quantidade_passageiros = models.PositiveIntegerField()
    modelo = models.CharField(max_length=100)
    cor = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateField(auto_now_add=True)
    obra_id = models.ForeignKey(Obras, on_delete=models.SET_NULL, null=True, blank=True, related_name='veiculos_associados') 

    class Meta:
        db_table = 'veiculos'

    def __str__(self):
        return f"{self.modelo} - {self.placa}"