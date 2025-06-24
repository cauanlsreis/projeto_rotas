from django.urls import path
from .views import OtimizarRotasAPIView, RotaListView,RotaDetailView


urlpatterns = [
    path('otimizar/', OtimizarRotasAPIView.as_view(), name='otimizar-rotas'),
    path('rotas/',  RotaListView.as_view(), name='listar-rotas'),
    path('rotas/<int:id>/', RotaDetailView.as_view(), name='rota-detail'),


]
