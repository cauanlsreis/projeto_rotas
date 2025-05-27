from django.urls import path
from .views import CadastroUsuarioAPIView, LoginView, UsuarioMeView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('cadastrar/', CadastroUsuarioAPIView.as_view(), name='cadastrar_usuario'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UsuarioMeView.as_view(), name='usuario_me'),
]