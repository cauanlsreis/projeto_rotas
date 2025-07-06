import requests
import json
from django.conf import settings
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

# Importações para autenticação OAuth 2.0
from google.oauth2 import service_account
import google.auth.transport.requests

# Importe seus models e serializers
from app.obras.models import Obras
from app.veiculos.models import veiculos
from app.funcionarios.models import Funcionarios
from .models import Rota
from .serializers import RotaSerializer

class OtimizarRotasAPIView(APIView):
    """
    API View para otimizar rotas de transporte de funcionários.
    Recebe um 'obra_id' e um 'veiculo_id' (opcional).
    Calcula as rotas de IDA e VOLTA, valida a capacidade dos veículos,
    chama a API Google Cloud Fleet Routing e salva os resultados.
    """
    permission_classes = [IsAuthenticated]

    def _chamar_api_otimizacao(self, project_id, headers, payload):
        """Função auxiliar para encapsular a chamada à API do Google."""
        url = f"https://routeoptimization.googleapis.com/v1/projects/{project_id}:optimizeTours"
        # Adiciona um timeout razoável para a chamada da API
        payload['timeout'] = '90s'
        api_response = requests.post(url, json=payload, headers=headers)
        api_response.raise_for_status()  # Lança um erro para respostas 4xx/5xx
        return api_response.json()

    def post(self, request):
        obra_id = request.data.get('obra_id')
        veiculo_id = request.data.get('veiculo_id')  # Campo opcional para selecionar um veículo

        if not obra_id:
            return Response({"erro": "O campo 'obra_id' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. BUSCAR DADOS ESSENCIAIS
            obra_destino = Obras.objects.get(id=obra_id)
            alojamentos_com_demanda = (
                Funcionarios.objects.filter(obra=obra_destino)
                .values('alojamento__id', 'alojamento__nome', 'alojamento__latitude', 'alojamento__longitude')
                .annotate(demanda_real=Count('id'))
                .filter(demanda_real__gt=0)
            )

            # 2. SELECIONAR VEÍCULOS PARA A OTIMIZAÇÃO
            if veiculo_id:
                # Cenário 1: Cliente escolheu um veículo específico
                try:
                    veiculo_selecionado = veiculos.objects.get(id=veiculo_id, ativo=True)
                    veiculos_para_otimizar = [veiculo_selecionado]
                except veiculos.DoesNotExist:
                    return Response({"erro": f"Veículo com id={veiculo_id} não encontrado ou está inativo."}, status=status.HTTP_404_NOT_FOUND)
            else:
                # Cenário 2: Cliente não escolheu, usar todos os veículos ativos
                veiculos_para_otimizar = list(veiculos.objects.filter(ativo=True, latitude__isnull=False, longitude__isnull=False))

            if not alojamentos_com_demanda or not veiculos_para_otimizar:
                return Response({"info": "Não há funcionários ou veículos disponíveis para a otimização."}, status=status.HTTP_404_NOT_FOUND)

            # 3. VALIDAR CAPACIDADE ANTES DE CHAMAR A API
            total_funcionarios = sum(item['demanda_real'] for item in alojamentos_com_demanda)
            capacidade_total_frota = sum(v.quantidade_passageiros for v in veiculos_para_otimizar)

            if total_funcionarios > capacidade_total_frota:
                return Response(
                    {"erro": "Capacidade de transporte insuficiente!",
                     "detalhes": f"A demanda é de {total_funcionarios} funcionários, mas a capacidade do(s) veículo(s) é de apenas {capacidade_total_frota}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 4. CONFIGURAR AUTENTICAÇÃO
            credentials_path = settings.GOOGLE_CREDENTIALS_PATH
            creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])
            project_id = creds.project_id
            auth_req = google.auth.transport.requests.Request()
            creds.refresh(auth_req)
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {creds.token}"}

            # 5. PREPARAR DADOS DOS VEÍCULOS (garantir que saiam e voltem para a base)
            vehicles_data = [{
                "label": f"{v.modelo} - {v.placa}",
                "start_waypoint": {"location": {"lat_lng": {"latitude": float(v.latitude), "longitude": float(v.longitude)}}},
                "end_waypoint": {"location": {"lat_lng": {"latitude": float(v.latitude), "longitude": float(v.longitude)}}},
                "load_limits": {"funcionarios": {"max_load": str(v.quantidade_passageiros)}}
            } for v in veiculos_para_otimizar]

            # 6. OTIMIZAÇÃO DA IDA (Alojamentos -> Obra)
            shipments_ida = [{
                "label": f"Coleta em {aloj['alojamento__nome']}",
                "pickups": [{"arrival_waypoint": {"location": {"lat_lng": {"latitude": float(aloj['alojamento__latitude']), "longitude": float(aloj['alojamento__longitude'])}}}, "load_demands": {"funcionarios": {"amount": str(aloj['demanda_real'])}}}],
                "deliveries": [{"arrival_waypoint": {"location": {"lat_lng": {"latitude": float(obra_destino.latitude), "longitude": float(obra_destino.longitude)}}}}]
            } for aloj in alojamentos_com_demanda]
            payload_ida = {"model": {"shipments": shipments_ida, "vehicles": vehicles_data}}
            resultado_ida = self._chamar_api_otimizacao(project_id, headers, payload_ida)

            # 7. OTIMIZAÇÃO DA VOLTA (Obra -> Alojamentos)
            shipments_volta = [{
                "label": f"Retorno para {aloj['alojamento__nome']}",
                "pickups": [{
                    "arrival_waypoint": {"location": {"lat_lng": {"latitude": float(obra_destino.latitude), "longitude": float(obra_destino.longitude)}}},
                    "load_demands": {"funcionarios": {"amount": str(aloj['demanda_real'])}}
                }],
                "deliveries": [{
                    "arrival_waypoint": {"location": {"lat_lng": {"latitude": float(aloj['alojamento__latitude']), "longitude": float(aloj['alojamento__longitude'])}}}
                }]
            } for aloj in alojamentos_com_demanda]

            payload_volta = {"model": {"shipments": shipments_volta, "vehicles": vehicles_data}}
            resultado_volta = self._chamar_api_otimizacao(project_id, headers, payload_volta)

            # 8. PROCESSAR E SALVAR RESULTADOS NO BANCO DE DADOS
            descricao_base = request.data.get('descricao', f"Transporte para {obra_destino.nome}")
            rotas_salvas = []
            
            def salvar_rotas(resultado_api, tipo_rota):
                for rota_gerada in resultado_api.get('routes', []):
                    placa_veiculo = rota_gerada.get('vehicleLabel', '').split(' - ')[-1]
                    veiculo_obj = veiculos.objects.filter(placa=placa_veiculo).first()
                    
                    rota_metrics = rota_gerada.get('metrics', {})
                    
                    nova_rota = Rota.objects.create(
                        descricao_transporte=f"{descricao_base} - {tipo_rota}",
                        obra_destino=obra_destino,
                        veiculo=veiculo_obj,
                        veiculo_label=rota_gerada.get('vehicleLabel', ''),
                        ordem_paradas=rota_gerada.get('visits', []),
                        distancia_total_metros=rota_metrics.get('travelDistanceMeters'),
                        duracao_total_segundos=int(rota_metrics.get('travelDuration', '0s').replace('s', ''))
                    )
                    rotas_salvas.append(RotaSerializer(nova_rota).data)
            
            salvar_rotas(resultado_ida, "IDA")
            salvar_rotas(resultado_volta, "VOLTA")

            # 9. MONTAR RESPOSTA FINAL PARA O CLIENTE
            distancia_ida_m = resultado_ida.get('metrics', {}).get('aggregatedRouteMetrics', {}).get('travelDistanceMeters', 0)
            distancia_volta_m = resultado_volta.get('metrics', {}).get('aggregatedRouteMetrics', {}).get('travelDistanceMeters', 0)
            distancia_total_frota_km = (distancia_ida_m + distancia_volta_m) / 1000

            # --- LÓGICA ATUALIZADA: Agrupar rotas e totais por veículo ---
            resumo_das_rotas = {}
            for rota in rotas_salvas:
                label = rota.get('veiculo_label')
                if not label:
                    continue
                
                # Se o veículo ainda não está no dicionário, inicializa sua estrutura
                if label not in resumo_das_rotas:
                    resumo_das_rotas[label] = {
                        "veiculo_label": label,
                        "distancia_total_metros": 0,
                        "duracao_total_segundos": 0,
                        "trechos_detalhados": []
                    }
                
                # Soma as métricas e anexa o trecho detalhado
                resumo_das_rotas[label]["distancia_total_metros"] += rota.get('distancia_total_metros') or 0
                resumo_das_rotas[label]["duracao_total_segundos"] += rota.get('duracao_total_segundos') or 0
                resumo_das_rotas[label]["trechos_detalhados"].append(rota)

            # Converter o dicionário para uma lista para a resposta final
            resumo_final_lista = []
            for label, data in resumo_das_rotas.items():
                data["distancia_total_km"] = round(data.pop("distancia_total_metros") / 1000, 2)
                resumo_final_lista.append(data)

            resposta_final = {
                "mensagem": f"{len(rotas_salvas)} trechos de rota (ida/volta) foram otimizados e salvos com sucesso.",
                "distancia_total_frota_km": round(distancia_total_frota_km, 2),
                "resumo_das_rotas": resumo_final_lista
            }
            return Response(resposta_final, status=status.HTTP_201_CREATED)

        # Bloco de tratamento de exceções
        except FileNotFoundError:
            return Response({"erro": "Arquivo de credenciais do Google não foi encontrado.", "detalhes": f"Verifique o caminho '{settings.GOOGLE_CREDENTIALS_PATH}'."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Obras.DoesNotExist:
            return Response({"erro": f"Obra com id={obra_id} não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.HTTPError as http_err:
            return Response({"erro": "Erro na chamada à API do Google", "detalhes": http_err.response.text}, status=http_err.response.status_code)
        except Exception as e:
            print(f"ERRO INESPERADO NA VIEW: {type(e).__name__} - {e}")
            return Response({"erro": "Ocorreu um erro interno no servidor.", "detalhes": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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