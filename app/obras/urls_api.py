from django.urls import path
from .views import ObrasCreateListView  # <-- certifique-se de importar essa view

urlpatterns = [
    path('', ObrasCreateListView.as_view(), name='obras-list-create'),
]
