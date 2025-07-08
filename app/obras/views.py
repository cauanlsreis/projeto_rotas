from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Obras
from .serializers import ObrasSerializer


class ObrasCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Obras.objects.all()
    serializer_class = ObrasSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "mensagem": "Obra cadastrada com sucesso!",
                "dados": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ObrasListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Obras.objects.all()
    serializer_class = ObrasSerializer


class ObrasDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Obras.objects.all()
    serializer_class = ObrasSerializer
