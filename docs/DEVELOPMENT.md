# DESENVOLVIMENTO - Segura

Guia completo para desenvolvimento e contribuição no projeto Segura.

## 📋 Índice

1. [Estrutura do Projeto](#estrutura-do-projeto)
2. [Configuração do Ambiente](#configuração-do-ambiente)
3. [Executando Localmente](#executando-localmente)
4. [Estrutura de Pastas](#estrutura-de-pastas)
5. [Padrões de Código](#padrões-de-código)
6. [API Endpoints](#api-endpoints)
7. [Banco de Dados](#banco-de-dados)
8. [PWA e Service Worker](#pwa-e-service-worker)
9. [Testes](#testes)
10. [Deploy](#deploy)

## Estrutura do Projeto

O Segura é um Progressive Web App (PWA) com arquitetura:
- **Backend**: Flask + SQLAlchemy
- **Frontend**: HTML5 + Vanilla JS + Tailwind CSS
- **Database**: SQLite
- **Auth**: Session-based com senha hasheada (pbkdf2)

## Configuração do Ambiente

### Pré-requisitos

- Python 3.8+
- pip
- Navegador moderno (Chrome, Firefox, Safari, Edge)

### Instalação

1. **Clonar repositório** (ou extrair arquivo)
```bash
cd App_para_mulher_localizacao
```

2. **Criar ambiente virtual** (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependências**
```bash
pip install -r requirements.txt
```

4. **Configurar variáveis de ambiente**
```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. **Executar setup inicial**
```bash
python scripts/setup.py
```

## Executando Localmente

### Opção 1: Script de Inicialização (Recomendado)

**Windows:**
```bash
scripts\iniciar.bat
```

**Linux/macOS:**
```bash
bash scripts/iniciar.sh
```

### Opção 2: Linha de Comando

```bash
python run.py
```

O servidor estará disponível em: `http://localhost:5000`

## Estrutura de Pastas

```
App_para_mulher_localizacao/
├── app/                          # Pacote principal Flask
│   ├── __init__.py              # Inicialização e exports
│   ├── models.py                # Modelos básicos (Contato, LocalSeguro)
│   ├── models_avancados.py      # Modelos avançados (Usuario, HistoricoSOS)
│   ├── routes.py                # Rotas da API
│   ├── routes_auth.py           # Rotas de autenticação
│   └── whatsapp_api.py          # Integração WhatsApp
├── templates/                    # Templates HTML Jinja2
│   ├── base.html                # Template base
│   ├── index.html               # Página principal
│   └── auth/
│       ├── login.html           # Formulário de login
│       └── registro.html        # Formulário de registro
├── static/                       # Arquivos estáticos
│   ├── css/
│   │   └── style.css            # Estilos customizados
│   ├── js/
│   │   ├── app.js               # Lógica principal
│   │   ├── panico.js            # Botão de pânico
│   │   ├── contatos.js          # CRUD de contatos
│   │   ├── locais.js            # CRUD de locais
│   │   └── sw.js                # Service Worker
│   ├── manifest.json            # Configuração PWA
│   └── icons/                   # Ícones do app
├── scripts/                      # Scripts utilitários
│   ├── setup.py                 # Setup inicial
│   ├── test_app.py              # Testes funcionais
│   ├── gerar_icones.py          # Gerador de ícones
│   ├── iniciar.bat              # Script Windows
│   └── iniciar.sh               # Script Unix
├── docs/                         # Documentação
│   ├── DEVELOPMENT.md           # Este arquivo
│   ├── WHATSAPP_SETUP.md        # Guia WhatsApp
│   ├── FILE_INDEX.md            # Índice de arquivos
│   └── IMPLEMENTACAO_RESUMO.md  # Resumo técnico
├── config/                       # Configurações
│   └── .env.example             # Template de variáveis
├── instance/                     # Instância da aplicação
│   └── app.db                   # Banco de dados SQLite
├── run.py                        # Entry point principal
├── requirements.txt              # Dependências Python
├── LICENSE                       # Licença
└── README.md                     # Documentação principal
```

## Padrões de Código

### Python

**Factory Pattern para Flask:**
```python
# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Blueprints para modularização:**
```python
# app/routes.py
from flask import Blueprint

main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/contatos', methods=['GET', 'POST'])
def gerenciar_contatos():
    # ...
```

**Modelos com SQLAlchemy:**
```python
# app/models.py
from app import db

class ContatoEmergencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    
    def to_dict(self):
        return {'id': self.id, 'nome': self.nome}
```

**Autenticação com Decorator:**
```python
# app/routes_auth.py
from functools import wraps
from flask import session, redirect

def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect('/auth/login')
        return f(*args, **kwargs)
    return decorada

@auth_bp.route('/perfil')
@login_requerido
def perfil():
    # Apenas usuários logados acessam
```

### JavaScript

**Modular e AJAX:**
```javascript
// static/js/contatos.js
async function criarContato(dados) {
    const response = await fetch('/api/contatos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });
    return response.json();
}
```

**Service Worker para offline:**
```javascript
// static/js/sw.js
self.addEventListener('fetch', event => {
    if (event.request.url.includes('/api/')) {
        // Network first para API
        event.respondWith(networkFirst(event.request));
    } else {
        // Cache first para assets
        event.respondWith(cacheFirst(event.request));
    }
});
```

## API Endpoints

### Autenticação

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/auth/registro` | Criar novo usuário | ❌ |
| POST | `/auth/login` | Login | ❌ |
| GET | `/auth/logout` | Logout | ✅ |
| GET | `/auth/perfil` | Obter perfil | ✅ |

### Contatos de Emergência

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/contatos` | Listar contatos | ✅ |
| POST | `/api/contatos` | Criar contato | ✅ |
| DELETE | `/api/contatos/<id>` | Deletar contato | ✅ |

### Locais Seguros

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/locais` | Listar locais | ✅ |
| POST | `/api/locais` | Criar local | ✅ |
| DELETE | `/api/locais/<id>` | Deletar local | ✅ |

### Geolocalização

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/localizacao` | Registrar localização | ✅ |

### SOS (Avançado)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/auth/historico-sos` | Listar SOS | ✅ |
| POST | `/auth/historico-sos` | Registrar novo SOS | ✅ |
| PATCH | `/auth/historico-sos/<id>` | Atualizar status SOS | ✅ |

### Exemplo de Requisição

```bash
# Criar contato
curl -X POST http://localhost:5000/api/contatos \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Maria Silva",
    "telefone": "(21) 98765-4321",
    "relacao": "Mãe"
  }'
```

## Banco de Dados

### Modelos

**ContatoEmergencia**
```
- id: Integer (PK)
- nome: String
- telefone: String
- relacao: String (Mãe, Pai, Amiga, etc)
- usuario_id: Foreign Key
```

**LocalSeguro**
```
- id: Integer (PK)
- nome: String
- tipo: String (Delegacia, Hospital, Casa amiga)
- endereco: String
- latitude: Float
- longitude: Float
- usuario_id: Foreign Key
```

**Usuario**
```
- id: Integer (PK)
- email: String (Unique)
- senha_hash: String (pbkdf2:sha256)
- nome: String
- data_criacao: DateTime
```

**HistoricoSOS**
```
- id: Integer (PK)
- usuario_id: Foreign Key
- contato_id: Foreign Key
- latitude: Float
- longitude: Float
- status: String (enviado, confirmado, cancelado)
- timestamp: DateTime
```

### Relacionamentos

```
Usuario 1-→ ∞ ContatoEmergencia (CASCADE)
Usuario 1-→ ∞ LocalSeguro (CASCADE)
Usuario 1-→ ∞ HistoricoSOS (CASCADE)
ContatoEmergencia 1-→ ∞ HistoricoSOS (CASCADE)
```

### Executar Query Manualmente

```python
# python
from run import create_app
from app import db
from app.models import ContatoEmergencia

app = create_app()
with app.app_context():
    contatos = ContatoEmergencia.query.all()
    for c in contatos:
        print(f"{c.nome}: {c.telefone}")
```

## PWA e Service Worker

### Configuração PWA

O arquivo `manifest.json` define o comportamento do app:

```json
{
  "name": "Segura",
  "short_name": "Segura",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#d946ef",
  "background_color": "#ffffff",
  "icons": [
    {
      "src": "/static/icons/icon-192.svg",
      "sizes": "192x192",
      "type": "image/svg+xml"
    }
  ]
}
```

### Service Worker

O arquivo `sw.js` implementa:

**Cache First** (para assets)
- CSS, JS, fonts
- Usa versão em cache se disponível
- Atualiza em background

**Network First** (para API)
- Tenta rede primeiro
- Fallback para cache
- Sempre atualiza cache

### Instalar como App

**Celular:**
1. Abra em navegador mobile
2. Menu → "Adicionar à tela inicial" ou "Instalar app"
3. O app funcionará offline (assets do cache)

**Desktop:**
1. Clique no ícone de instalação na barra de URL
2. Ou: Menu → "Instalar Segura"

## Testes

### Testes Automatizados

```bash
python scripts/test_app.py
```

Testa:
- ✅ Conexão com servidor
- ✅ Registro e login
- ✅ CRUD de contatos
- ✅ CRUD de locais
- ✅ Geolocalização
- ✅ Configuração PWA

### Teste Manual

1. Abra `http://localhost:5000`
2. Crie uma conta
3. Faça login
4. Cadastre contatos e locais
5. Teste o botão de pânico
6. Verifique no navegador Dev Tools → Application → Manifests

## Deploy

### Heroku (recomendado para PWA)

1. **Instalar Heroku CLI**
```bash
# https://devcenter.heroku.com/articles/heroku-cli
```

2. **Fazer login**
```bash
heroku login
```

3. **Criar aplicação**
```bash
heroku create seu-app-segura
```

4. **Configurar variáveis**
```bash
heroku config:set WHATSAPP_API_URL=https://...
heroku config:set WHATSAPP_TOKEN=seu_token
```

5. **Deploy**
```bash
git push heroku main
```

### Replit

1. Importe repositório no Replit
2. Configure `.env` com variáveis
3. Execute `python run.py`
4. Compartilhe o link gerado

### Seu Servidor (VPS/Cloud)

1. SSH para servidor
2. Clone repositório
3. Instale Python e pip
4. Execute `python scripts/setup.py`
5. Configure certificado SSL (Let's Encrypt)
6. Configure nginx/apache como proxy reverso
7. Use systemd para autostart

**Exemplo nginx.conf:**
```nginx
server {
    listen 443 ssl;
    server_name seu-dominio.com;
    
    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:5000;
    }
}
```

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"

```bash
# Instale dependências
pip install -r requirements.txt
```

### Erro: "Address already in use"

Porta 5000 está em uso. Mude em run.py:
```python
app.run(port=5001)
```

### Service Worker não funciona

1. Verifique se acessa por HTTPS (ou localhost)
2. Abra DevTools → Application → Service Workers
3. Desregistre e recarregue página
4. Verifique se `manifest.json` existe

### Geolocalização não funciona

1. Abra pelo celular (não funciona com IP privado)
2. Use HTTPS ou localhost
3. Permita acesso à localização no navegador

## Próximos Passos

- [ ] Integrar WhatsApp Business API
- [ ] Adicionar notificações push
- [ ] Implementar mapas interativos
- [ ] Adicionar chat em tempo real
- [ ] Análise de segurança e penetration testing
- [ ] Testes de carga
- [ ] Interface admin
- [ ] Multilíngue

## Suporte

Para dúvidas ou problemas:
1. Verifique a documentação em `/docs`
2. Abra uma issue no GitHub
3. Envie email para suporte

---

**Última atualização:** 2024
**Versão:** 1.0.0
