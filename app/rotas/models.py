from django.db import models
from app.veiculos.models import veiculos
from app.obras.models import Obras

class Rota(models.Model):
    # Campos para agrupar as rotas de uma mesma operação
    descricao_transporte = models.CharField(max_length=255, help_text="Nome da operação. Ex: Transporte Obra X 05/07/2025", default='')
    obra_destino = models.ForeignKey(Obras, on_delete=models.SET_NULL, null=True)
    data_geracao = models.DateTimeField(auto_now_add=True)
    
    # Campos específicos de cada rota gerada pela API
    veiculo = models.ForeignKey(veiculos, on_delete=models.SET_NULL, null=True)
    veiculo_label = models.CharField(max_length=100, blank=True, null=True) # Para guardar o label ex: 'Onix - ABC1234'
    ordem_paradas = models.JSONField(help_text="Detalhes completos da rota, incluindo visitas, tempos e distâncias")
    distancia_total_metros = models.IntegerField(null=True, blank=True)
    duracao_total_segundos = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'rotas_otimizadas'
    
    def __str__(self):
        return f"Rota para {self.veiculo_label} - {self.descricao_transporte}"