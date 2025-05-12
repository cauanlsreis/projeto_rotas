from django.urls import path
from .views import CadastroUsuarioAPIView

urlpatterns = [
    path('cadastrar/', CadastroUsuarioAPIView.as_view(), name='cadastrar_usuario'),
]