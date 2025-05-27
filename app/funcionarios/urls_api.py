from django.urls import path
from .views import FuncionariosCreateListView, FuncionariosListView

urlpatterns = [
    path('', FuncionariosCreateListView.as_view(), name='cadastrar_funcionario'),
    path('visualizar', FuncionariosListView.as_view(), name='listar-funcionarios'),
    path('listar', FuncionariosListView.as_view(), name='funcionarios-listar'),  # GET para listar
]
