from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Projeto Rotas API",
        default_version='v1',
        description="Documentação da API do Projeto Rotas",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('app.usuarios.urls_api')),
    path('api/alojamentos/', include('app.alojamentos.urls_api')),
    path('api/obras/', include('app.obras.urls_api')),
    path('api/veiculos/', include('app.veiculos.urls_api')),
    path('api/funcionarios/', include('app.funcionarios.urls_api')),
    path('api/rotas/', include('app.rotas.urls_api')),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
