from django.urls import path
from .views import VeiculosCreateView, VeiculosListView, VeiculosDetailView

urlpatterns = [
    path('cadastrar/', VeiculosCreateView.as_view(), name='veiculos-create'),
    path('', VeiculosListView.as_view(), name='veiculos-list'),
    path('<int:pk>/', VeiculosDetailView.as_view(),name='veiculos-detail')
]
