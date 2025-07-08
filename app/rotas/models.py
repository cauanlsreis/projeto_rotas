from django.db import models
from app.veiculos.models import veiculos
from app.obras.models import Obras

class Rota(models.Model):
    # Campos para agrupar as rotas de uma mesma operação
    descricao_transporte = models.CharField(max_length=255, help_text="Nome da operação. Ex: Transporte Obra X 05/07/2025", default='')
    obra_destino = models.ForeignKey(Obras, on_delete=models.SET_NULL, null=True)
    data_geracao = models.DateTimeField(auto_now_add=True)

    # --- NOVO CAMPO ADICIONADO ---
    TIPO_TRECHO_CHOICES = [
        ('IDA', 'Ida'),
        ('VOLTA', 'Volta'),
    ]
    tipo_trecho = models.CharField(max_length=5, choices=TIPO_TRECHO_CHOICES, default='IDA')

    # Campos específicos de cada rota gerada pela API
    veiculo = models.ForeignKey(veiculos, on_delete=models.SET_NULL, null=True)
    veiculo_label = models.CharField(max_length=100, blank=True, null=True)
    ordem_paradas = models.JSONField(help_text="Detalhes completos da rota, incluindo visitas, tempos e distâncias")

    polyline = models.TextField(blank=True, null=True, help_text="Polyline codificada para desenhar a rota no mapa")

    distancia_total_metros = models.IntegerField(null=True, blank=True)
    duracao_total_segundos = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'rotas_otimizadas'

    def _str_(self):
        return f"Rota para {self.veiculo_label} - {self.descricao_transporte} ({self.tipo_trecho})"