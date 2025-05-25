from django.urls import path
from .views import FuncionariosCreateView
from .views import FuncionariosListView

urlpatterns = [
    path('', FuncionariosCreateView.as_view(), name='cadastrar_funcionario'),
    path('visualizar', FuncionariosListView.as_view(), name='listar-funcionarios')
]
