# 🛡️ Guia de Desenvolvimento e Deploy

## 🚀 Quick Start (5 minutos)

### 1. Clone o repositório
```bash
git clone <seu-repo>
cd App_para_mulher_localizacao
```

### 2. Crie ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale dependências
```bash
pip install -r requirements.txt
```

### 4. Execute setup automático
```bash
python setup.py
```

### 5. Inicie o servidor
```bash
python app.py
```

Abra [http://localhost:5000](http://localhost:5000) 🎉

---

## 🔑 Variáveis de Ambiente

Copie e customize `.env.example`:

```bash
cp .env.example .env
```

```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua_chave_secreta_super_segura_aqui

# Database
DATABASE_URL=sqlite:///app.db

# WhatsApp (opcional, deixe vazio para testar com wa.me)
WHATSAPP_API_URL=https://graph.instagram.com/v18.0
WHATSAPP_PHONE_ID=seu_phone_id
WHATSAPP_TOKEN=seu_token_aqui
```

---

## 📚 Estrutura de Arquivos

```
App_para_mulher_localizacao/
│
├── app.py                    # Aplicação principal Flask
├── models.py                 # Modelos de DB (Contatos, Locais)
├── models_avancados.py       # Modelos (Usuários, Histórico SOS)
├── routes.py                 # Rotas básicas e API
├── routes_auth.py            # Rotas de autenticação
│
├── whatsapp_api.py          # Integração WhatsApp Business API
├── gerar_icones.py          # Gerador de ícones PWA
├── setup.py                 # Script de inicialização
│
├── static/
│   ├── css/style.css        # Estilos customizados
│   ├── js/
│   │   ├── app.js           # Script principal
│   │   ├── panico.js        # Botão de pânico
│   │   ├── contatos.js      # CRUD contatos
│   │   ├── locais.js        # CRUD locais
│   │   └── sw.js            # Service Worker (PWA)
│   ├── manifest.json        # Configuração PWA
│   └── icon-*.svg           # Ícones do app
│
├── templates/
│   ├── base.html            # Template base
│   ├── index.html           # Página principal
│   ├── login.html           # Página de login
│   └── registro.html        # Página de registro
│
├── requirements.txt         # Dependências Python
├── .env.example             # Exemplo de .env
├── .gitignore              # Arquivos ignorados pelo Git
├── README.md               # Documentação principal
├── WHATSAPP_SETUP.md       # Configuração WhatsApp
└── DEVELOPMENT.md          # Este arquivo
```

---

## 🧪 Testes e Validações

### Testar APIs com curl

#### Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@exemplo.com",
    "senha": "senha123"
  }'
```

#### Criar Contato
```bash
curl -X POST http://localhost:5000/api/contatos \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Maria Silva",
    "telefone": "21987654321",
    "relacao": "Mãe"
  }'
```

#### Listar Contatos
```bash
curl http://localhost:5000/api/contatos
```

#### Listar Locais
```bash
curl http://localhost:5000/api/locais
```

---

## 🐛 Debugging

### Ativar modo debug
```bash
export FLASK_DEBUG=1
python app.py
```

### Acessar banco de dados
```bash
# Instale sqlite3 (já vem no Python)
sqlite3 instance/app.db

# Alguns comandos úteis
sqlite> .tables                          # Listar tabelas
sqlite> SELECT * FROM usuarios;          # Ver usuários
sqlite> SELECT * FROM contatos_emergencia; # Ver contatos
```

### Limpar banco de dados
```bash
rm instance/app.db
python setup.py
```

---

## 🚀 Deploy em Produção

### Heroku

1. Instale Heroku CLI:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. Crie arquivo `Procfile`:
```
web: gunicorn app:create_app()
```

3. Deploy:
```bash
heroku login
heroku create nome-do-app
git push heroku main
```

### Railway.app

1. Conecte seu GitHub
2. Selecione o repositório
3. Configure variáveis de ambiente
4. Deploy automático ✅

### Servidor Próprio (Linux)

```bash
# 1. SSH no servidor
ssh usuario@seu-servidor.com

# 2. Clone repositório
git clone <seu-repo>
cd App_para_mulher_localizacao

# 3. Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Instale Gunicorn
pip install gunicorn

# 5. Rode o app
gunicorn --workers 4 --bind 0.0.0.0:5000 app:create_app()

# 6. (Opcional) Configure nginx como proxy reverso
# (veja documentação do nginx)
```

---

## 🔐 Checklist de Segurança

Antes de ir para produção:

- [ ] `SECRET_KEY` é uma string aleatória forte
- [ ] `FLASK_DEBUG=False` em produção
- [ ] Senhas são hashadas com pbkdf2:sha256
- [ ] HTTPS está ativado
- [ ] Variáveis sensíveis estão no `.env`
- [ ] Database URL apontava para servidor seguro
- [ ] Rate limiting implementado na API
- [ ] CORS está configurado corretamente
- [ ] Log de erros está em arquivo, não no console
- [ ] Backups automáticos do banco de dados

---

## 📦 Versionamento

Use semantic versioning (MAJOR.MINOR.PATCH):

```bash
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

---

## 🤝 Contributing

1. Fork o projeto
2. Crie branch: `git checkout -b feature/nova-feature`
3. Commit: `git commit -am 'Add nova feature'`
4. Push: `git push origin feature/nova-feature`
5. Open Pull Request

---

## 📝 Changelog

### v1.0.0 (2024-04)
- ✅ MVP inicial
- ✅ Botão de pânico com WhatsApp
- ✅ CRUD de contatos e locais
- ✅ PWA com offline support
- ✅ Sistema de autenticação

### v1.1.0 (planejado)
- [ ] Histórico detalhado de SOS
- [ ] Compartilhamento em tempo real
- [ ] Notificações push
- [ ] Relatórios de segurança

---

## 📞 Suporte

- GitHub Issues: [link]
- Email: segura@exemplo.com
- Discord: [link]

---

**Última atualização:** Abril 2024
**Versão:** 1.0.0-beta
