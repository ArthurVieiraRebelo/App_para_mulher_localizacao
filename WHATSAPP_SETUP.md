# 📱 Configuração WhatsApp Business API

Guia completo para integrar a **WhatsApp Business API** no app Segura.

## 🔧 Opções de Integração

### Opção 1: WhatsApp Web (Rápido - Atual)
- Redireciona para `wa.me/NUMERO?text=MENSAGEM`
- Funciona sem credenciais
- Limitado a envios manuais
- ✅ Já implementado no MVP

### Opção 2: WhatsApp Business API Oficial (Robusto)
- Autentificação com chave de API
- Envios automáticos de mensagens
- Histórico e rastreamento
- Integrações avançadas
- 🔜 Código já preparado em `whatsapp_api.py`

---

## 📋 Como Configurar WhatsApp Business API

### 1️⃣ Obtenha uma Conta Meta Business

1. Acesse [developers.facebook.com](https://developers.facebook.com)
2. Crie uma conta de desenvolvedor (ou use existente)
3. Vá para **Meus Apps** → **Criar App**
4. Escolha **Negócio** como tipo de app

### 2️⃣ Ative WhatsApp

1. No app criado, procure por **WhatsApp**
2. Clique em **Configurar**
3. Siga as instruções de verificação

### 3️⃣ Obtenha as Credenciais

Na seção **API** do seu app, você encontrará:

- **API URL**: `https://graph.instagram.com/v18.0`
- **Phone ID**: ID do número telefônico registrado
- **Token**: Chave de acesso pessoal

### 4️⃣ Configure no App

Crie/atualize o arquivo `.env`:

```env
# WhatsApp Business API
WHATSAPP_API_URL=https://graph.instagram.com/v18.0
WHATSAPP_PHONE_ID=seu_phone_id_aqui
WHATSAPP_TOKEN=seu_token_aqui
```

### 5️⃣ Teste a Integração

```bash
python -c "
from whatsapp_api import WhatsAppAPI
wa = WhatsAppAPI()
resultado = wa.enviar_mensagem_panico(
    '5521987654321',  # Número com código do país
    latitude=-23.5505,
    longitude=-46.6333,
    nome_usuario='Teste'
)
print(resultado)
"
```

---

## 🔑 Tipos de Tokens

| Tipo | Duração | Uso |
|------|---------|-----|
| **Temporary** | 1 hora | Testes rápidos |
| **User Access Token** | ~60 dias | Desenvolvimento |
| **App Access Token** | Indefinido | Produção ✅ |

Para produção, crie um **App Access Token** nas configurações do app.

---

## 📨 Formatos de Mensagens Suportadas

### Texto Simples
```python
{
    "type": "text",
    "text": {
        "preview_url": true,
        "body": "Sua mensagem aqui..."
    }
}
```

### Localização
```python
{
    "type": "location",
    "location": {
        "latitude": -23.5505,
        "longitude": -46.6333,
        "name": "Minha localização",
        "address": "Av. Principal, 100"
    }
}
```

### Documento
```python
{
    "type": "document",
    "document": {
        "link": "https://exemplo.com/doc.pdf",
        "caption": "Documento importante"
    }
}
```

---

## ✅ Checklist de Deploy

- [ ] Número de telefone verificado com Meta
- [ ] Token App Access gerado
- [ ] `.env` configurado com credenciais
- [ ] API testada em ambiente de sandbox
- [ ] Mensagens de teste enviadas com sucesso
- [ ] Histórico de SOS sendo salvo no banco
- [ ] Rate limiting implementado (em produção)

---

## 🆘 Troubleshooting

### Erro: "Invalid phone ID"
- Verifique se `WHATSAPP_PHONE_ID` está correto
- Confirme que o número foi registrado na conta

### Erro: "Invalid token"
- Token expirou? Gere novo em Meta Business
- Token tem permissões de WhatsApp? Verifique escopos

### Mensagem não chega
- Verifique se número de destino inclui código do país (ex: 55)
- Teste com número que já usa WhatsApp

### Rate Limiting
- Meta limita a ~80 mensagens/segundo em volume
- Implemente fila de mensagens para picos

---

## 📚 Documentação Oficial

- [Meta WhatsApp Cloud API Docs](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Postman Collection](https://www.postman.com/meta-official/)

---

## 🔐 Segurança

⚠️ **IMPORTANTE:**
- Nunca commite tokens no Git
- Use variáveis de ambiente
- Implemente rate limiting
- Valide números de telefone
- Criptografe dados sensíveis
- Use HTTPS em produção

---

**Status Atual:** Código preparado, aguardando credenciais Meta para ativar 🚀
