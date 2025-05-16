from django.urls import path
from .views import VeiculoCreateListView

urlpatterns = [
    path('', VeiculoCreateListView.as_view(), name='veiculos'),
]
