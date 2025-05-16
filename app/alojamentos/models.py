from django.db import models

class Alojamentos(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=150)
    numero  = models.CharField(max_length=10)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    longitude = models.DecimalField(max_digits=9,decimal_places=6)
    data_cadastro = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'alojamentos'

    def __str__(self):
        return f"{self.nome} - {self.cidade}/{self.estado}"  

