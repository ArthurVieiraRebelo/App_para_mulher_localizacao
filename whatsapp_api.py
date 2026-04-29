"""
Integração com WhatsApp Business API.
Configuração e funções para enviar mensagens via API oficial.
"""

import requests
import os
from datetime import datetime

class WhatsAppAPI:
    """
    Cliente para WhatsApp Business API.
    Mais robusto que redirecionar para wa.me/
    """
    
    def __init__(self):
        self.api_url = os.getenv('WHATSAPP_API_URL', '')
        self.api_token = os.getenv('WHATSAPP_TOKEN', '')
        self.phone_id = os.getenv('WHATSAPP_PHONE_ID', '')
    
    def enviar_mensagem_panico(self, numero_destino, latitude=None, longitude=None, nome_usuario='Usuária'):
        """
        Envia mensagem de pânico via WhatsApp Business API.
        
        Args:
            numero_destino: Número do WhatsApp (formato: 55XXXXXXXXXX)
            latitude: Latitude da localização
            longitude: Longitude da localização
            nome_usuario: Nome de quem está enviando
        
        Returns:
            dict com resultado da requisição
        """
        
        # Sem credenciais configuradas, retorna aviso
        if not self.api_token or not self.phone_id:
            return {
                'sucesso': False,
                'mensagem': 'WhatsApp API não configurada. Use wa.me como fallback.'
            }
        
        # Cria link do mapa
        link_mapa = f'https://maps.google.com/?q={latitude},{longitude}' if latitude and longitude else 'Localização não disponível'
        
        # Mensagem formatada
        mensagem = f"""🆘 *SITUAÇÃO DE EMERGÊNCIA* 🆘

{nome_usuario} está em perigo e precisa de ajuda URGENTE!

📍 *Localização:*
{link_mapa}

⏰ *Horário:* {datetime.now().strftime('%H:%M:%S')}

*POR FAVOR PROCURE AJUDA OU AVISE AS AUTORIDADES*

---
Mensagem enviada pelo app Segura"""
        
        payload = {
            'messaging_product': 'whatsapp',
            'to': numero_destino,
            'type': 'text',
            'text': {
                'preview_url': True,
                'body': mensagem
            }
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                f'{self.api_url}/messages',
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'sucesso': True,
                    'mensagem': 'Mensagem enviada com sucesso',
                    'message_id': data.get('messages', [{}])[0].get('id')
                }
            else:
                return {
                    'sucesso': False,
                    'mensagem': f'Erro: {response.status_code}',
                    'detalhes': response.text
                }
        
        except requests.RequestException as e:
            return {
                'sucesso': False,
                'mensagem': f'Erro na requisição: {str(e)}'
            }
    
    def enviar_localizacao_compartilhada(self, numero_destino, latitude, longitude):
        """
        Envia localização em tempo real (compartilhamento contínuo).
        Útil para seguir movimento da pessoa.
        """
        
        if not self.api_token or not self.phone_id:
            return {'sucesso': False, 'mensagem': 'API não configurada'}
        
        payload = {
            'messaging_product': 'whatsapp',
            'to': numero_destino,
            'type': 'location',
            'location': {
                'latitude': latitude,
                'longitude': longitude,
                'name': 'Minha localização atual',
                'address': 'Compartilhado automaticamente'
            }
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                f'{self.api_url}/messages',
                json=payload,
                headers=headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False


# Função helper para usar em rotas
def enviar_alerta_whatsapp(numero, latitude, longitude, nome='Usuária'):
    """
    Wrapper simples para enviar alerta WhatsApp.
    """
    wa = WhatsAppAPI()
    return wa.enviar_mensagem_panico(numero, latitude, longitude, nome)
