from django.urls import path
from .views import ObrasCreateView, ObrasListView, ObrasDetailView 

urlpatterns = [
    path('cadastrar/', ObrasCreateView.as_view(), name='obras-create'),
    path('', ObrasListView.as_view(),name='obras-list'),
    path('<int:pk>/', ObrasDetailView.as_view(),name='obras-detail')
]
