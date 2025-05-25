from django.urls import path
from .views import AlojamentosCreateView
from .views import AlojamentosListView

urlpatterns = [
    path('', AlojamentosCreateView.as_view(),name='alojamento-create'),
    path('visualizar', AlojamentosListView.as_view(),name='alojamento-list-view'),
]