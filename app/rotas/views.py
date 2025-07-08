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
    permission_classes = [IsAuthenticated]

    def _chamar_api_otimizacao(self, project_id, headers, payload):
        url = f"https://routeoptimization.googleapis.com/v1/projects/{project_id}:optimizeTours"
        payload['timeout'] = '90s'
        api_response = requests.post(url, json=payload, headers=headers)
        api_response.raise_for_status()
        return api_response.json()

    def post(self, request):
        obra_id = request.data.get('obra_id')
        veiculo_id = request.data.get('veiculo_id')

        if not obra_id:
            return Response({"erro": "O campo 'obra_id' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. BUSCAR DADOS
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

            # 2. SELECIONAR VEÍCULOS
            if veiculo_id:
                try:
                    veiculo_selecionado = veiculos.objects.get(id=veiculo_id, ativo=True)
                    veiculos_para_otimizar = [veiculo_selecionado]
                except veiculos.DoesNotExist:
                    return Response({"erro": f"Veículo com id={veiculo_id} não encontrado ou está inativo."}, status=status.HTTP_404_NOT_FOUND)
            else:
                veiculos_para_otimizar = list(veiculos.objects.filter(ativo=True, latitude__isnull=False, longitude__isnull=False))

            if not alojamentos_com_demanda or not veiculos_para_otimizar:
                return Response({"info": "Não há funcionários ou veículos disponíveis para a otimização."}, status=status.HTTP_404_NOT_FOUND)

            # 3. VALIDAR CAPACIDADE
            total_funcionarios = sum(item['demanda_real'] for item in alojamentos_com_demanda)
            capacidade_total_frota = sum(v.quantidade_passageiros for v in veiculos_para_otimizar)

            if total_funcionarios > capacidade_total_frota:
                return Response(
                    {"erro": "Capacidade de transporte insuficiente!",
                     "detalhes": f"A demanda é de {total_funcionarios} funcionários, mas a capacidade do(s) veículo(s) é de apenas {capacidade_total_frota}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 4. AUTENTICAÇÃO E PREPARAÇÃO
            credentials_path = settings.GOOGLE_CREDENTIALS_PATH
            creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])
            project_id = creds.project_id
            auth_req = google.auth.transport.requests.Request()
            creds.refresh(auth_req)
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {creds.token}"}

            vehicles_data = [{
                "label": f"{v.modelo} - {v.placa}",
                "start_waypoint": {"location": {"lat_lng": {"latitude": float(v.latitude), "longitude": float(v.longitude)}}},
                "end_waypoint": {"location": {"lat_lng": {"latitude": float(v.latitude), "longitude": float(v.longitude)}}},
                "load_limits": {"funcionarios": {"max_load": str(v.quantidade_passageiros)}}
            } for v in veiculos_para_otimizar]

            # 6. OTIMIZAÇÃO DA IDA
            shipments_ida = [{"label": f"Coleta em {aloj['alojamento__nome']}", "pickups": [{"arrival_waypoint": {"location": {"lat_lng": {"latitude": float(aloj['alojamento__latitude']), "longitude": float(aloj['alojamento__longitude'])}}}, "load_demands": {"funcionarios": {"amount": str(aloj['demanda_real'])}}}], "deliveries": [{"arrival_waypoint": {"location": {"lat_lng": {"latitude": float(obra_destino.latitude), "longitude": float(obra_destino.longitude)}}}}]} for aloj in alojamentos_com_demanda]
            payload_ida = {
                "model": {"shipments": shipments_ida, "vehicles": vehicles_data},
                "populatePolylines": True
            }
            resultado_ida = self._chamar_api_otimizacao(project_id, headers, payload_ida)

            # 7. OTIMIZAÇÃO DA VOLTA
            shipments_volta = [{"label": f"Retorno para {aloj['alojamento__nome']}", "pickups": [{"arrival_waypoint": {"location": {"lat_lng": {"latitude": float(obra_destino.latitude), "longitude": float(obra_destino.longitude)}}}, "load_demands": {"funcionarios": {"amount": str(aloj['demanda_real'])}}}], "deliveries": [{"arrival_waypoint": {"location": {"lat_lng": {"latitude": float(aloj['alojamento__latitude']), "longitude": float(aloj['alojamento__longitude'])}}}}]} for aloj in alojamentos_com_demanda]
            payload_volta = {
                "model": {"shipments": shipments_volta, "vehicles": vehicles_data},
                "populatePolylines": True
            }
            resultado_volta = self._chamar_api_otimizacao(project_id, headers, payload_volta)

            # 8. PROCESSAR E SALVAR RESULTADOS
            descricao_base = request.data.get('descricao', f"Transporte para {obra_destino.nome}")
            rotas_salvas = []

            def salvar_rotas(resultado_api, tipo_rota):
                # --- DEBUG: Imprime a resposta da API no log de erros ---
                print(f"--- RESPOSTA DO GOOGLE PARA {tipo_rota} ---")
                print(json.dumps(resultado_api, indent=2))
                print("-----------------------------------------")

                for rota_gerada in resultado_api.get('routes', []):
                    placa_veiculo = rota_gerada.get('vehicleLabel', '').split(' - ')[-1]
                    veiculo_obj = veiculos.objects.filter(placa=placa_veiculo).first()
                    rota_metrics = rota_gerada.get('metrics', {})
                    encoded_polyline = rota_gerada.get('routePolyline', {}).get('points')

                    nova_rota = Rota.objects.create(
                        descricao_transporte=descricao_base,
                        tipo_trecho=tipo_rota,
                        obra_destino=obra_destino,
                        veiculo=veiculo_obj,
                        veiculo_label=rota_gerada.get('vehicleLabel', ''),
                        ordem_paradas=rota_gerada.get('visits', []),
                        polyline=encoded_polyline,
                        distancia_total_metros=rota_metrics.get('travelDistanceMeters'),
                        duracao_total_segundos=int(rota_metrics.get('travelDuration', '0s').replace('s', ''))
                    )
                    rotas_salvas.append(RotaSerializer(nova_rota).data)

            salvar_rotas(resultado_ida, "IDA")
            salvar_rotas(resultado_volta, "VOLTA")

            # 9. MONTAR RESPOSTA FINAL
            distancia_total_frota_km = (resultado_ida.get('metrics', {}).get('aggregatedRouteMetrics', {}).get('travelDistanceMeters', 0) + resultado_volta.get('metrics', {}).get('aggregatedRouteMetrics', {}).get('travelDistanceMeters', 0)) / 1000

            resumo_das_rotas = {}
            for rota in rotas_salvas:
                label = rota.get('veiculo_label')
                if not label: continue
                if label not in resumo_das_rotas:
                    resumo_das_rotas[label] = {"veiculo_label": label, "distancia_total_metros": 0, "duracao_total_segundos": 0, "trechos_detalhados": []}
                resumo_das_rotas[label]["distancia_total_metros"] += rota.get('distancia_total_metros') or 0
                resumo_das_rotas[label]["duracao_total_segundos"] += rota.get('duracao_total_segundos') or 0
                resumo_das_rotas[label]["trechos_detalhados"].append(rota)

            resumo_final_lista = []
            for label, data in resumo_das_rotas.items():
                data["distancia_total_km"] = round(data.pop("distancia_total_metros") / 1000, 2)
                resumo_final_lista.append(data)

            resposta_final = {
                "mensagem": f"{len(rotas_salvas)} trechos de rota (ida/volta) foram otimizados e salvos.",
                "distancia_total_frota_km": round(distancia_total_frota_km, 2),
                "resumo_das_rotas": resumo_final_lista
            }
            return Response(resposta_final, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"ERRO INESPERADO NA VIEW: {type(e).__name__} - {e}")
            return Response({"erro": "Ocorreu um erro interno no servidor.", "detalhes": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- Views de Listagem e Detalhe (COM CORREÇÃO E AGRUPAMENTO) ---
class RotaListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RotaSerializer

    def get_queryset(self):
        queryset = Rota.objects.all().order_by('-data_geracao', 'descricao_transporte', 'veiculo_label')
        descricao = self.request.query_params.get('descricao_transporte', None)
        if descricao is not None:
            queryset = queryset.filter(descricao_transporte=descricao)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        rotas_serializadas = self.get_serializer(queryset, many=True).data
        operacoes = {}
        for rota in rotas_serializadas:
            descricao = rota.get('descricao_transporte')
            if descricao not in operacoes:
                operacoes[descricao] = []
            operacoes[descricao].append(rota)

        resposta_final = []
        for descricao, trechos in operacoes.items():
            resumo_por_veiculo = {}
            distancia_total_operacao_m = 0
            id_rota = trechos[0].get('id') if trechos else None

            for trecho in trechos:
                label = trecho.get('veiculo_label')
                distancia_trecho_m = trecho.get('distancia_total_metros') or 0
                distancia_total_operacao_m += distancia_trecho_m

                if label not in resumo_por_veiculo:
                    resumo_por_veiculo[label] = {
                        "veiculo_label": label,
                        "distancia_total_metros": 0,
                        "duracao_total_segundos": 0,
                        "trechos_detalhados": []
                    }

                resumo_por_veiculo[label]["distancia_total_metros"] += distancia_trecho_m
                resumo_por_veiculo[label]["duracao_total_segundos"] += trecho.get('duracao_total_segundos') or 0
                resumo_por_veiculo[label]["trechos_detalhados"].append(trecho)

            lista_veiculos_formatada = []
            for label, data in resumo_por_veiculo.items():
                data["distancia_total_km"] = round(data.pop("distancia_total_metros") / 1000, 2)
                lista_veiculos_formatada.append(data)

            operacao_formatada = {
                "id_rota": id_rota,
                "descricao_transporte": descricao,
                "distancia_total_operacao_km": round(distancia_total_operacao_m / 1000, 2),
                "resumo_por_veiculo": lista_veiculos_formatada
            }
            resposta_final.append(operacao_formatada)

        return Response(resposta_final)

class RotaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhe, atualização e exclusão de uma rota.
    Ao deletar, apaga toda a operação de transporte (todos os trechos com a mesma descrição).
    """
    permission_classes = [IsAuthenticated]
    queryset = Rota.objects.all()
    serializer_class = RotaSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        """
        Sobrescreve o método destroy para deletar toda a operação.
        """
        instance = self.get_object()
        descricao_para_deletar = instance.descricao_transporte
        if descricao_para_deletar:
            rotas_da_operacao = Rota.objects.filter(descricao_transporte=descricao_para_deletar)
            count = rotas_da_operacao.count()
            rotas_da_operacao.delete()
            return Response(
                {"mensagem": f"{count} trechos de rota da operação '{descricao_para_deletar}' foram deletados com sucesso."},
                status=status.HTTP_204_NO_CONTENT
            )
        return super().destroy(request, *args, **kwargs)
