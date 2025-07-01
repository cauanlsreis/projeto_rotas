import requests
import json
from django.conf import settings
from django.db.models import Count
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

# Importações para autenticação OAuth 2.0 com carregamento explícito
from google.oauth2 import service_account
import google.auth.transport.requests

# Importe seus models e serializers
from app.alojamentos.models import Alojamentos
from app.obras.models import Obras
from app.veiculos.models import veiculos
from app.funcionarios.models import Funcionarios
from .models import Rota
from .serializers import RotaSerializer

class OtimizarRotasAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):

         # 1. Validação e busca da obra
        # 2. Montagem do payload para os shipments
        # 3. Montagem da lista de veículos disponíveis
        # 4. Configuração da autenticação (Service Account) e geração do token
        # 5. Payload globalStartTime e globalEndTime
        # 6. Chamada à API do Google Maps Fleet Routing
        # 7. Tratamento de erros e resposta

        obra_id = request.data.get('obra_id')
        if not obra_id:
            return Response({"erro": "O campo 'obra_id' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Buscar dados
            obra_destino = Obras.objects.get(id=obra_id)
            alojamentos_com_demanda = (
                Funcionarios.objects.filter(obra=obra_destino)
                .values(
                    'alojamento__id',
                    'alojamento__nome',
                    'alojamento__latitude',
                    'alojamento__longitude'
                )
                .annotate(demanda_real=Count('id'))
                .filter(demanda_real__gt=0)
            )
            if not alojamentos_com_demanda:
                return Response(
                    {"info": "Nenhum funcionário encontrado para esta obra nos alojamentos."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 2. Montar o payload correto para os shipments
            shipments = []
            for aloj in alojamentos_com_demanda:
                shipments.append(
                    {
                        "label": f"Coleta no {aloj['alojamento__nome']}",
                        "pickups": [
                            {
                                "arrival_waypoint": {
                                    "location": {
                                        "lat_lng": {
                                            "latitude": float(aloj['alojamento__latitude']),
                                            "longitude": float(aloj['alojamento__longitude'])
                                        }
                                    }
                                },
                                "load_demands": {
                                    "funcionarios": {
                                        "amount": str(aloj['demanda_real'])
                                    }
                                }
                            }
                        ],
                        "deliveries": [
                            {
                                "arrival_waypoint": {
                                    "location": {
                                        "lat_lng": {
                                            "latitude": float(obra_destino.latitude),
                                            "longitude": float(obra_destino.longitude)
                                        }
                                    }
                                }
                            }
                        ]
                    }
                )

            # 3. Montar a lista de veículos
            veiculos_disponiveis = veiculos.objects.filter(
                ativo=True,
                latitude__isnull=False,
                longitude__isnull=False
            )
            if not veiculos_disponiveis:
                return Response(
                    {"info": "Nenhum veículo ativo com localização definida foi encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )

            vehicles_data = []
            for v in veiculos_disponiveis:
                vehicles_data.append(
                    {
                        "label": f"{v.modelo} - {v.placa}",
                        "start_waypoint": {
                            "location": {
                                "lat_lng": {
                                    "latitude": float(v.latitude),
                                    "longitude": float(v.longitude)
                                }
                            }
                        },
                        "end_waypoint": {
                            "location": {
                                "lat_lng": {
                                    "latitude": float(v.latitude),
                                    "longitude": float(v.longitude)
                                }
                            }
                        },
                        "load_limits": {
                            "funcionarios": {
                                "max_load": str(v.quantidade_passageiros)
                            }
                        }
                    }
                )

            # 4. Configurar autenticação
            credentials_path = settings.GOOGLE_CREDENTIALS_PATH
            scopes = ['https://www.googleapis.com/auth/cloud-platform']

            creds = service_account.Credentials.from_service_account_file(
                credentials_path, scopes=scopes
            )
            project_id = creds.project_id
            auth_req = google.auth.transport.requests.Request()
            creds.refresh(auth_req)  # Atualiza token


            # 5. Payload 
            agora = datetime.utcnow().replace(microsecond=0) 
            global_start = agora.strftime("%Y-%m-%dT%H:%M:%SZ")
            global_end = (agora + timedelta(hours=10)).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
            
            payload = {
                "model": {
                    "shipments": shipments,
                    "vehicles": vehicles_data,
                    "globalStartTime": global_start,  
                    "globalEndTime": global_end       
                },
                "solvingMode": "DEFAULT_SOLVE"        
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds.token}"
            }

            url = f"https://routeoptimization.googleapis.com/v1/projects/{project_id}:optimizeTours"
            api_response = requests.post(url, json=payload, headers=headers)
            api_response.raise_for_status()
            result_data = api_response.json()

           
            # --- LINHAS MODIFICADAS PARA O UPGRADE COMEÇAM AQUI ---
            total_distance_km = 0
            # A API já fornece a distância total agregada para todos os veículos
            if 'metrics' in result_data and 'aggregatedRouteMetrics' in result_data['metrics']:
                if 'travelDistanceMeters' in result_data['metrics']['aggregatedRouteMetrics']:
                    total_distance_km = result_data['metrics']['aggregatedRouteMetrics']['travelDistanceMeters'] / 1000
            
            result_data['total_distance_all_vehicles_km'] = total_distance_km
            # --- LINHAS MODIFICADAS PARA O UPGRADE TERMINAM AQUI ---


            return Response(result_data, status=status.HTTP_200_OK)

        except FileNotFoundError:
            return Response(
                {"erro": "Arquivo de credenciais do Google não foi encontrado.",
                 "detalhes": f"Verifique o caminho '{settings.GOOGLE_CREDENTIALS_PATH}'."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Obras.DoesNotExist:
            return Response({"erro": f"Obra com id={obra_id} não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.HTTPError as http_err:
            return Response(
                {"erro": "Erro na chamada à API do Google", "detalhes": http_err.response.text},
                status=http_err.response.status_code
            )
        except Exception as e:
            print(f"ERRO INESPERADO NA VIEW: {e}")
            return Response(
                {"erro": "Ocorreu um erro interno no servidor.", "detalhes": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
# Views de Listagem e Detalhe
class RotaListView(generics.ListAPIView):

    """
    Listagem de todas as rotas cadastradas, ordenadas por data de geração (mais recentes primeiro).

    Requer autenticação.
    """
    permission_classes = [IsAuthenticated]
    queryset = Rota.objects.all().order_by('-data_geracao')
    serializer_class = RotaSerializer

class RotaDetailView(generics.RetrieveUpdateDestroyAPIView):

    """
    Detalhe, atualização e exclusão de uma rota específica.

    Identificação da rota via 'id' na URL.
    Requer autenticação.
    """
    permission_classes = [IsAuthenticated]
    queryset = Rota.objects.all()
    serializer_class = RotaSerializer
    lookup_field = 'id'
