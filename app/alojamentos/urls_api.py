from django.urls import path
from .views import AlojamentosListCreateView

urlpatterns = [
    path('', AlojamentosListCreateView.as_view(),name='alojamento-list-create'),
]