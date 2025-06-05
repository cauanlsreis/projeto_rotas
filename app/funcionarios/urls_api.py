from django.urls import path
from .views import FuncionariosCreateView, FuncionariosListView, FuncionariosDetailView

urlpatterns = [
    path('cadastrar/', FuncionariosCreateView.as_view(), name='funcionarios-create'),
    path('', FuncionariosListView.as_view(), name='funcionarios-list'),
    path('<int:pk>/', FuncionariosDetailView.as_view(), name='funcionarios-detail'),  # GET para listar
]
