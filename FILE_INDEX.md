# 📁 Índice Completo de Arquivos

Todos os arquivos do projeto Segura com descrição e função.

## 🏗️ Arquivos de Configuração

| Arquivo | Descrição |
|---------|-----------|
| `requirements.txt` | Dependências Python (Flask, SQLAlchemy, Gunicorn, etc) |
| `.env.example` | Template de variáveis de ambiente |
| `.gitignore` | Arquivos ignorados pelo Git |

## 🐍 Backend (Python/Flask)

| Arquivo | Descrição | Função |
|---------|-----------|--------|
| **app.py** | Aplicação principal Flask | Cria app, inicializa DB, registra blueprints |
| **models.py** | Modelos de dados básicos | ContatoEmergencia, LocalSeguro |
| **models_avancados.py** | Modelos avançados | Usuario, HistoricoSOS |
| **routes.py** | Rotas principais | GET/POST/DELETE para contatos e locais |
| **routes_auth.py** | Rotas de autenticação | Login, registro, logout, histórico SOS |
| **whatsapp_api.py** | Integração WhatsApp | Envio de mensagens via API |

## 🚀 Scripts de Inicialização

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| **setup.py** | Setup automático | `python setup.py` - Inicializa tudo |
| **test_app.py** | Testes interativos | `python test_app.py` - Valida funcionalidades |
| **iniciar.bat** | Inicialização (Windows) | `iniciar.bat` - Ativa venv + app |
| **iniciar.sh** | Inicialização (Linux/Mac) | `./iniciar.sh` - Ativa venv + app |
| **gerar_icones.py** | Gerador de ícones | `python gerar_icones.py` - Cria SVGs |

## 🎨 Frontend (HTML/CSS/JavaScript)

### Templates HTML
| Arquivo | Página | Função |
|---------|--------|--------|
| `templates/base.html` | Template base | Estrutura comum (header, footer) |
| `templates/index.html` | Página principal | Botão pânico, abas contatos/locais |
| `templates/login.html` | Página de login | Autenticação de usuários |
| `templates/registro.html` | Página de registro | Criar nova conta |

### CSS
| Arquivo | Descrição |
|---------|-----------|
| `static/css/style.css` | Estilos customizados (animações, cards, responsive) |

### JavaScript
| Arquivo | Função |
|---------|--------|
| `static/js/app.js` | Script principal (abas, requisições, geolocalização) |
| `static/js/panico.js` | Lógica botão de pânico (WhatsApp redirect) |
| `static/js/contatos.js` | CRUD de contatos de emergência |
| `static/js/locais.js` | CRUD de locais seguros |
| `static/js/sw.js` | Service Worker (PWA, cache, offline) |

### PWA
| Arquivo | Descrição |
|---------|-----------|
| `static/manifest.json` | Configuração PWA (nome, ícones, cores) |
| `static/icon-*.svg` | Ícones do app (gerados) |

## 📚 Documentação

| Arquivo | Conteúdo | Público? |
|---------|----------|----------|
| **README.md** | Visão geral do projeto | ✅ Sim (versão pública) |
| **DEVELOPMENT.md** | Guia desenvolvimento + deploy | ✅ Equipe |
| **WHATSAPP_SETUP.md** | Configuração WhatsApp API | ✅ Equipe |
| **IMPLEMENTACAO_RESUMO.md** | O que foi implementado | 📖 Referência |
| **FILE_INDEX.md** | Este arquivo | 📖 Referência |

## 📊 Resumo Estatístico

### Linhas de Código
```
Backend (Python):        ~1200 linhas
Frontend (HTML/JS/CSS):  ~1500 linhas
Documentação:            ~1000 linhas
Scripts:                 ~800 linhas
────────────────────────────────────
Total:                   ~4500 linhas
```

### Arquivos por Tipo
- 🐍 Python: 10 arquivos
- 🌐 Web (HTML/CSS/JS): 9 arquivos
- 📚 Documentação: 6 arquivos
- ⚙️ Scripts: 4 arquivos
- 📋 Configuração: 3 arquivos

**Total: 32 arquivos**

## 🔗 Dependências Externas

### Backend
- **Flask** - Framework web
- **Flask-SQLAlchemy** - ORM para banco de dados
- **SQLAlchemy** - SQL Toolkit
- **Werkzeug** - Utilities (password hashing)
- **requests** - HTTP client
- **python-dotenv** - Variáveis de ambiente
- **gunicorn** - WSGI server (produção)

### Frontend
- **Tailwind CSS** - Framework CSS (CDN)

## 🏃 Fluxo de Execução

```
iniciar.bat/sh
    ↓
setup.py (cria venv, DB, ícones)
    ↓
app.py (Flask app starts)
    ↓
http://localhost:5000
    ├─ GET / → index.html
    ├─ POST /auth/registro → register user
    ├─ POST /auth/login → login user
    ├─ POST /api/contatos → create contact
    ├─ POST /api/panico → panic button
    └─ etc...
```

## 📈 Funcionalidades por Arquivo

### Autenticação
- ✅ Registro (templates/registro.html + routes_auth.py)
- ✅ Login (templates/login.html + routes_auth.py)
- ✅ Sessions (Flask)
- ✅ Password hashing (Werkzeug)

### Contatos
- ✅ Criar (routes.py + static/js/contatos.js)
- ✅ Listar (routes.py + static/js/contatos.js)
- ✅ Deletar (routes.py + static/js/contatos.js)

### Locais Seguros
- ✅ Criar (routes.py + static/js/locais.js)
- ✅ Listar (routes.py + static/js/locais.js)
- ✅ Google Maps link (static/js/locais.js)
- ✅ Deletar (routes.py + static/js/locais.js)

### Pânico
- ✅ Capturar localização (static/js/panico.js)
- ✅ WhatsApp redirect (static/js/panico.js)
- ✅ WhatsApp API (whatsapp_api.py - ready)
- ✅ Histórico SOS (models_avancados.py + routes_auth.py)

### PWA
- ✅ Service Worker (static/js/sw.js)
- ✅ Manifest (static/manifest.json)
- ✅ Offline support (static/js/sw.js)
- ✅ Ícones (gerar_icones.py)

## 🔧 Manutenção

### Adicionar Nova Feature
1. Criar modelo em `models.py` ou `models_avancados.py`
2. Adicionar rotas em `routes.py` ou `routes_auth.py`
3. Criar template HTML (se necessário)
4. Adicionar JavaScript em `static/js/`
5. Atualizar README.md
6. Testar com `test_app.py`

### Encontrar Funcionalidade X
- **Login?** → templates/login.html + routes_auth.py
- **Botão Pânico?** → static/js/panico.js
- **WhatsApp?** → whatsapp_api.py
- **Banco de dados?** → models.py + models_avancados.py
- **Rotas/API?** → routes.py + routes_auth.py

### Encontrar Bug em X
- **Interface UI?** → templates/ + static/css/style.css
- **Comportamento JS?** → static/js/
- **Lógica backend?** → routes.py
- **Banco de dados?** → models.py
- **Autenticação?** → routes_auth.py + models_avancados.py

---

## 🎯 Quick Reference

### Comandos Úteis
```bash
# Setup inicial
python setup.py

# Rodar app
python app.py

# Testar funcionalidades
python test_app.py

# Gerar ícones
python gerar_icones.py

# Limpar banco (recria do zero)
rm instance/app.db
python setup.py
```

### URLs Principais
| URL | Método | Função |
|-----|--------|--------|
| `/` | GET | Página principal |
| `/auth/login` | GET/POST | Login |
| `/auth/registro` | GET/POST | Registro |
| `/api/contatos` | GET/POST | Contatos |
| `/api/locais` | GET/POST | Locais |
| `/api/historico-sos` | GET/POST | Histórico SOS |

---

**Última atualização:** Abril 2024
**Versão:** 1.0.0-beta
**Status:** ✅ Completo e pronto para testes
