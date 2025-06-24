from django.db import models
from app.veiculos.models import veiculos

class Rota(models.Model):
    veiculo = models.ForeignKey(veiculos, on_delete=models.CASCADE)
    ordem_paradas = models.JSONField()  # Armazena lat/lng em ordem
    data_geracao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rotas_otimizadas'
    
    def __str__(self):
        return f"Rota do veículo {self.veiculo} em {self.data_otimizacao}"