# Índice de Arquivos - Segura

Referência rápida de todos os arquivos do projeto com descrições.

## 📂 Estrutura Completa

### 🟦 PASTA: `app/` - Código da Aplicação

| Arquivo | Linhas | Descrição |
|---------|--------|-----------|
| `__init__.py` | 25 | Factory pattern, db, exports de modelos |
| `models.py` | 40 | ContatoEmergencia, LocalSeguro |
| `models_avancados.py` | 60 | Usuario (com hash), HistoricoSOS |
| `routes.py` | 120 | API endpoints (contatos, locais) |
| `routes_auth.py` | 150 | Auth endpoints (registro, login, SOS) |
| `whatsapp_api.py` | 80 | Integração WhatsApp Business API |

**Total**: 475 linhas Python no core da app

---

### 🟨 PASTA: `templates/` - HTML

| Arquivo | Descrição |
|---------|-----------|
| `base.html` | Template base (header, nav, footer) |
| `index.html` | Página principal (4 abas: Dashboard, Contatos, Locais, SOS) |
| `auth/login.html` | Formulário de login |
| `auth/registro.html` | Formulário de registro |

**Total**: 4 templates Jinja2

---

### 🟩 PASTA: `static/` - Assets

#### CSS
| Arquivo | Descrição |
|---------|-----------|
| `css/style.css` | Estilos customizados (animações, cards) |

#### JavaScript (Módulos)
| Arquivo | Linhas | Descrição |
|---------|--------|-----------|
| `js/app.js` | 150 | Navegação abas, AJAX helpers, geoloc |
| `js/panico.js` | 120 | Botão pânico, modal seleção contato |
| `js/contatos.js` | 100 | CRUD contatos com validação |
| `js/locais.js` | 100 | CRUD locais, links Google Maps |
| `js/sw.js` | 130 | Service Worker (cache + network) |

#### PWA
| Arquivo | Descrição |
|---------|-----------|
| `manifest.json` | Metadados PWA (nome, ícones, display) |

#### Ícones
| Pasta | Descrição |
|--------|-----------|
| `icons/` | Ícones gerados (SVG 192x192, 512x512) |

**Total**: ~600 linhas JavaScript em 5 módulos

---

### 🟪 PASTA: `scripts/` - Utilitários

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| `setup.py` | Python | Verifica deps, cria .env, init DB, gera ícones |
| `test_app.py` | Python | Testa todas funcionalidades (7 testes) |
| `gerar_icones.py` | Python | Gera SVGs de ícones 192x512 |
| `iniciar.bat` | Batch | Start server Windows (verifica deps) |
| `iniciar.sh` | Bash | Start server Unix/macOS |

**Total**: 5 scripts

---

### 📚 PASTA: `docs/` - Documentação

| Arquivo | Descrição |
|---------|-----------|
| `DEVELOPMENT.md` | Guia completo de desenvolvimento |
| `WHATSAPP_SETUP.md` | Setup WhatsApp (MVP + Business API) |
| `FILE_INDEX.md` | Este arquivo |
| `IMPLEMENTACAO.md` | Resumo técnico do que foi implementado |

---

### ⚙️ PASTA: `config/` - Configuração

| Arquivo | Descrição |
|---------|-----------|
| `.env.example` | Template de variáveis de ambiente |

**Criar `.env` copiando este arquivo durante setup**

---

### 🗄️ PASTA: `instance/` - Instância Aplicação

| Arquivo | Descrição |
|---------|-----------|
| `app.db` | Banco SQLite (criado automaticamente) |

---

### 📦 RAIZ DO PROJETO

| Arquivo | Descrição |
|---------|-----------|
| `run.py` | Entry point principal (substitui app.py) |
| `requirements.txt` | Dependências Python |
| `README.md` | Documentação principal |
| `LICENSE` | Licença MIT |

---

## 🎯 Guia de Uso por Arquivo

### Para Iniciar o Servidor
```bash
# Simples (com script)
scripts/iniciar.bat           # Windows
bash scripts/iniciar.sh       # Linux/macOS

# Manual
python run.py                 # Direto
```

### Para Testar Funcionalidades
```bash
python tests/test_app.py    # Roda 7 testes automatizados
```

### Para Setup Inicial
```bash
python scripts/setup.py       # Verifica deps, cria DB, ícones
```

### Para Editar Lógica da App
```
app/models.py              → Estrutura de dados
app/models_avancados.py    → Usuario, SOS, hash
app/routes.py              → Endpoints API
app/routes_auth.py         → Autenticação, Login
app/whatsapp_api.py        → WhatsApp
```

### Para Editar Frontend
```
templates/base.html        → Layout base
templates/index.html       → Interface principal
static/js/app.js           → Lógica geral
static/js/panico.js        → Botão SOS
static/js/contatos.js      → Gerenciar contatos
static/js/locais.js        → Gerenciar locais
```

### Para PWA/Offline
```
static/js/sw.js            → Service Worker (cache)
static/manifest.json       → Metadados PWA
scripts/gerar_icones.py    → Gerar ícones
```

### Para Configuração
```
.env                        → Variáveis ambiente (criar)
.env.example               → Template (referência)
config/                    → Pasta de config
```

---

## 📊 Estatísticas

### Linhas de Código
```
Backend (Python)     ~475 linhas
Frontend (JS)        ~600 linhas
Templates (HTML)     ~400 linhas
Styles (CSS)         ~150 linhas
─────────────────
Total                ~1625 linhas
```

### Arquivos por Tipo
```
Python      12 arquivos
JavaScript   5 arquivos
HTML         4 arquivos
CSS          1 arquivo
JSON         1 arquivo
Bash/Batch   2 arquivos
Markdown     4 documentos
─────────────────
Total       29 arquivos
```

### Modelos de Dados
```
Usuario               1 tabela
ContatoEmergencia    1 tabela
LocalSeguro          1 tabela
HistoricoSOS         1 tabela
─────────────────
Total               4 tabelas
```

### Endpoints
```
Autenticação         4 rotas
API (Contatos)       3 rotas
API (Locais)         3 rotas
API (Geoloc)         1 rota
SOS (Histórico)      3 rotas
─────────────────
Total               14 rotas
```

---

## 🔍 Procurando Algo?

### Botão de Pânico
→ `static/js/panico.js` + `app/routes.py`

### Autenticação
→ `app/routes_auth.py` + `app/models_avancados.py`

### WhatsApp
→ `app/whatsapp_api.py` + `static/js/panico.js`

### Service Worker / Offline
→ `static/js/sw.js` + `static/manifest.json`

### Banco de Dados
→ `app/models.py` + `app/models_avancados.py`

### Design / UI
→ `templates/base.html` + `static/css/style.css` + Tailwind CDN

### Teste de Funcionalidades
→ `tests/test_app.py`

### Setup / Inicialização
→ `scripts/setup.py` + `run.py`

---

## 📝 Convenções

### Nomes de Arquivo
- **Python**: `snake_case` (ex: `whatsapp_api.py`)
- **JavaScript**: `snake_case` (ex: `panico.js`)
- **HTML**: `snake_case` (ex: `registro.html`)
- **CSS**: `style.css`

### Estrutura de Pasta
```
app/              → Código Python
scripts/          → Scripts utilitários
templates/        → Templates HTML (+ subpastas)
static/           → Arquivos estáticos (JS, CSS, imgs)
docs/             → Documentação
config/           → Configuração
```

### URLs Pattern
```
/                        → Página principal
/auth/login             → Login
/auth/registro          → Registro
/api/contatos          → CRUD contatos
/api/locais            → CRUD locais
/api/localizacao       → Geoloc
/auth/historico-sos    → SOS history
```

---

## 🚀 Próximos Arquivos a Criar

Se estender o projeto:

```
tests/
├── test_auth.py         → Testes autenticação
├── test_api.py          → Testes API
└── test_models.py       → Testes modelos

static/
├── js/admin.js          → Painel admin
├── css/admin.css        → Estilos admin
└── icons/              → Mais ícones customizados

templates/
├── admin/               → Painel admin
└── componentes/         → Componentes reutilizáveis

app/
├── admin.py            → Rotas admin
└── utils.py            → Funções utilitárias
```

---

**Última atualização:** 2024
**Versão:** 1.0.0
