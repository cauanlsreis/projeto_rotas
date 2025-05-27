from django.urls import path
from .views import AlojamentosCreateListView, AlojamentosListView

urlpatterns = [
    path('', AlojamentosCreateListView.as_view(),name='alojamento-create'),
    path('visualizar', AlojamentosListView.as_view(),name='alojamento-list-view'),
    path('listar', AlojamentosListView.as_view(), name='alojamento-listar'),  # GET para listar
]