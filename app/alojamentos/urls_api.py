from django.urls import path
from .views import AlojamentosCreateListView, AlojamentosListView, AlojamentosDetailView

urlpatterns = [
    path('cadastrar/', AlojamentosCreateListView.as_view(),name='alojamento-create'),
    path('', AlojamentosListView.as_view(),name='alojamento-list'),
    path('<int:pk>/', AlojamentosDetailView.as_view(),name='alojamento-detail')
]