# WhatsApp Setup - Segura

Guia completo para configurar a integração com WhatsApp Business API.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Opção 1: MVP (wa.me - Imediato)](#opção-1-mvp-wame---imediato)
3. [Opção 2: Business API (Completo)](#opção-2-business-api---completo)
4. [Testes](#testes)
5. [Troubleshooting](#troubleshooting)

## Visão Geral

O Segura oferece 2 formas de integração WhatsApp:

| Aspecto | MVP (wa.me) | Business API |
|--------|-----------|--------------|
| **Setup** | ⏱️ 5 minutos | ⏱️ 30 minutos |
| **Custo** | Grátis | R$ 0,05-0,15 por mensagem |
| **Automático** | ❌ Manual | ✅ Automático |
| **Histórico** | ⚠️ Limitado | ✅ Completo |
| **Melhor para** | Testes/MVP | Produção |

## Opção 1: MVP (wa.me - Imediato)

**SEM configuração necessária!** Funciona com link wa.me direto.

### Como Funciona

Quando usuária clica botão pânico:
1. App obtém localização (lat/long)
2. Gera link WhatsApp: `https://wa.me/5521987654321?text=...`
3. Abre WhatsApp automaticamente com mensagem pré-digitada
4. Usuária clica enviar

### Pré-requisitos

- ✅ WhatsApp instalado no celular
- ✅ Número salvo com código de país (+55)
- ✅ Acesso à internet

### Usar Imediatamente

```javascript
// static/js/panico.js já implementa wa.me
const whatsappLink = `https://wa.me/${contatoTelefone}?text=${mensagem}`;
window.open(whatsappLink);
```

**Pronto! Não precisa fazer nada mais.**

### Limitações

- Não funciona se usuária não tem WhatsApp
- Não há confirmação automática de recebimento
- Histórico fica no WhatsApp, não no app
- Não funciona em computador (sem WhatsApp Web)

---

## Opção 2: Business API - Completo

Para envio automático sem ação do usuário. Recomendado para produção.

### 1. Criar Conta Meta Business

#### 1.1 Acesso Initial

Visite: https://developers.facebook.com/

```
Clique em "Meus Aplicativos" → Criar Aplicativo
└─ Tipo: Business
└─ Nome: Segura
└─ Email: seu@email.com
```

#### 1.2 Adicionar Produto WhatsApp

```
Dashboard → + Adicionar Produto
└─ WhatsApp
└─ Próximo
```

### 2. Obter Credentials

#### 2.1 Seu Número de Telefone WhatsApp

Na seção "Números de Telefone":

```
Clique em "Adicionar Número de Telefone"
└─ Código país: 55 (Brasil)
└─ Seu número: 21987654321
└─ Verificar via SMS
```

**Copie o "Business Account ID":**
```
WABA_ID = 100123456789012
```

#### 2.2 Token de Acesso Permanente

Na seção "Ferramentas" → "Tokens de Sistema":

```
Clique em "Gerar Token"
└─ Permissões: whatsapp_business_messaging
└─ Expiração: Nunca
```

**Copie o token:**
```
WHATSAPP_TOKEN = EAABxxxxxxxxxxx...
```

#### 2.3 URL da API

Padrão Meta (não muda):
```
WHATSAPP_API_URL = https://graph.instagram.com/v18.0/
```

Ou usar versão mais recente:
```
WHATSAPP_API_URL = https://graph.instagram.com/v19.0/
```

### 3. Configurar Arquivo .env

Edite `.env` e adicione:

```env
# WhatsApp Business API
WHATSAPP_API_URL=https://graph.instagram.com/v19.0
WHATSAPP_TOKEN=EAABxxxxxxxxxxx...
WHATSAPP_PHONE_ID=100123456789012

# Número de telefone para receber SOS
WHATSAPP_OWNER_NUMBER=+5521987654321
```

⚠️ **SEGURANÇA**: Nunca committe .env com credenciais reais!

### 4. Testar Conexão

```bash
# Terminal
curl -X POST \
  "https://graph.instagram.com/v19.0/100123456789012/messages" \
  -H "Authorization: Bearer EAABxxxxxxxxxxx..." \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "5521987654321",
    "type": "text",
    "text": {
      "body": "Teste de conexão WhatsApp"
    }
  }'
```

Resposta sucesso:
```json
{
  "messages": [
    {
      "id": "wamid.xxx=",
      "message_status": "accepted"
    }
  ]
}
```

### 5. Como Funciona no Código

```python
# app/whatsapp_api.py
from app.whatsapp_api import WhatsAppAPI

# Instanciar
wa = WhatsAppAPI()

# Enviar mensagem de pânico
resposta = wa.enviar_mensagem_panico(
    numero_destino="+5521987654321",
    nome_usuario="João Silva"
)

# Enviar localização
resposta = wa.enviar_localizacao_compartilhada(
    numero_destino="+5521987654321",
    latitude=-23.5505,
    longitude=-46.6333
)
```

### 6. Implementar no Panic Button

Quando usuária clica pânico:

```python
# routes.py (pseudocódigo)
@api_bp.route('/panico', methods=['POST'])
@login_requerido
def panico():
    usuario = session.get('usuario_id')
    dados = request.json
    lat, lng = dados['latitude'], dados['longitude']
    
    # 1. Registrar SOS no banco
    sos = HistoricoSOS(
        usuario_id=usuario,
        latitude=lat,
        longitude=lng,
        status='enviado'
    )
    db.session.add(sos)
    
    # 2. Enviar via WhatsApp Business API
    wa = WhatsAppAPI()
    for contato in ContatoEmergencia.query.filter_by(usuario_id=usuario):
        wa.enviar_mensagem_panico(
            numero_destino=contato.telefone,
            nome_usuario=session.get('nome')
        )
        wa.enviar_localizacao_compartilhada(
            numero_destino=contato.telefone,
            latitude=lat,
            longitude=lng
        )
    
    db.session.commit()
    return {'status': 'SOS enviado'}, 200
```

---

## Testes

### Teste 1: Conexão API

```bash
python -c "from app.whatsapp_api import WhatsAppAPI; wa = WhatsAppAPI(); print('✓ API OK')"
```

### Teste 2: Enviar Mensagem de Teste

```python
from app.whatsapp_api import WhatsAppAPI

wa = WhatsAppAPI()
resposta = wa.enviar_mensagem_panico(
    numero_destino="+5521987654321",
    nome_usuario="Usuária Teste"
)
print(resposta)
```

### Teste 3: Via App

1. Acesse http://localhost:5000
2. Crie uma conta
3. Cadastre um contato com seu número
4. Clique em "Testar WhatsApp"
5. Verifique se recebeu mensagem no WhatsApp

---

## Troubleshooting

### Erro: "WHATSAPP_TOKEN não configurado"

**Solução:** Adicione token ao `.env`

```env
WHATSAPP_TOKEN=EAABxxxxxxxxxxx...
```

### Erro: "Número inválido"

**Causa:** Formato incorreto do telefone

**Solução:** Use `+55` + 9 dígitos
```
✓ Correto:   +5521987654321
✗ Incorreto: 21 98765-4321
✗ Incorreto: (21) 98765-4321
```

### Erro: "401 Unauthorized"

**Causa:** Token expirado ou inválido

**Solução:** 
1. Gere novo token em https://developers.facebook.com/
2. Atualize `.env`
3. Reinicie servidor

### Erro: "403 Forbidden - Invalid Phone Number ID"

**Causa:** Phone ID incorreto

**Solução:**
1. Verifique em Meta Dashboard → WhatsApp → Números de Telefone
2. Copie o ID exato
3. Atualize `.env`

### Mensagem não chega

**Verificar:**
1. ✅ Token válido
2. ✅ Número tem WhatsApp Business
3. ✅ Número está verificado em Meta Dashboard
4. ✅ Número não está na lista de bloqueados
5. ✅ API URL está correta (v18.0 ou v19.0)

**Debug:**
```python
from app.whatsapp_api import WhatsAppAPI
import json

wa = WhatsAppAPI()
# Ver resposta da API
resposta = wa.enviar_mensagem_panico("+5521987654321", "Teste")
print(json.dumps(resposta, indent=2))
```

---

## FAQ

**P: Preciso usar Business API ou wa.me funciona?**
R: wa.me funciona sem setup. Business API para automação em produção.

**P: Qual o custo?**
R: wa.me = grátis. Business API = ~R$ 0,05-0,15 por mensagem.

**P: Funciona com números normais de WhatsApp?**
R: wa.me = sim. Business API = precisa de número comercial.

**P: Preciso de website/domínio?**
R: Não. Localhost funciona para testes.

**P: Posso testar em celular?**
R: Sim! Use IP da máquina: `http://SEU_IP:5000`

**P: Como receber confirmação de leitura?**
R: Business API com webhooks (avançado).

---

## Recursos Úteis

- **Meta Dashboard**: https://developers.facebook.com/
- **Documentação WhatsApp API**: https://developers.facebook.com/docs/whatsapp/
- **Status API**: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/phone-number
- **Webhook Reference**: https://developers.facebook.com/docs/whatsapp/webhooks/

---

**Última atualização:** 2024
**Versão:** 1.0.0
