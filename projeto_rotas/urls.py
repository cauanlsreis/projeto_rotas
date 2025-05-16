from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/usuarios/', include('app.usuarios.urls_api')),
    path('api/alojamentos/', include('app.alojamentos.urls_api')),
    path('api/obras/',include('app.obras.urls_api')),
    path('api/veiculos/',include('app.veiculos.urls_api')),
    path('api/funcionarios/',include('app.funcionarios.urls_api'))
]