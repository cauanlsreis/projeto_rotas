from django.urls import path
from .views import FuncionariosCreateView

urlpatterns = [
    path('', FuncionariosCreateView.as_view(), name='cadastrar_funcionario'),
]
