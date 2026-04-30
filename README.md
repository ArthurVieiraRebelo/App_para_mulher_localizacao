# 🛡️ Segura - App de Segurança Pessoal

MVP de Progressive Web App (PWA) focado em segurança pessoal de mulheres, com botão de pânico, geolocalização e integração WhatsApp.

## 🚀 Funcionalidades

- **Botão de Pânico**: Envio de localização via WhatsApp em um clique
- **Contatos de Emergência**: Cadastro e gerenciamento de contatos
- **Locais Seguros**: Mapa de delegacias, hospitais e casas de amigos próximas
- **PWA**: Funciona offline e pode ser instalado como app nativo
- **Mobile-First**: Interface otimizada para celular

## 📋 Stack

### Backend
- **Python 3.9+**
- **Flask** - Framework web
- **SQLAlchemy** - ORM
- **SQLite** - Banco de dados

### Frontend
- **HTML5**
- **CSS3 + Tailwind CSS**
- **JavaScript puro** (sem frameworks)

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone <seu-repo>
cd App_para_mulher_localizacao
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Crie arquivo de variáveis de ambiente
```bash
cp .env.example .env
```

### 5. Execute a aplicação
```bash
python app.py
```

O app estará disponível em `http://localhost:5000`

## 📁 Estrutura do Projeto

```
App_para_mulher_localizacao/
├── static/
│   ├── css/
│   │   └── style.css          # Estilos customizados
│   ├── js/
│   │   ├── app.js             # Script principal
│   │   ├── panico.js          # Lógica do botão de pânico
│   │   ├── contatos.js        # CRUD de contatos
│   │   ├── locais.js          # CRUD de locais
│   │   └── sw.js              # Service Worker (PWA)
│   └── manifest.json          # Manifest PWA
├── templates/
│   ├── base.html              # Template base
│   └── index.html             # Página inicial
├── app.py                     # Aplicação principal Flask
├── models.py                  # Modelos do banco de dados
├── routes.py                  # Rotas e endpoints API
├── requirements.txt           # Dependências Python
├── .env.example               # Exemplo de variáveis
└── README.md                  # Este arquivo
```

## 🔌 API Endpoints

### Contatos de Emergência

- **GET** `/api/contatos` - Lista todos os contatos
- **POST** `/api/contatos` - Cria novo contato
  ```json
  {
    "nome": "Maria",
    "telefone": "21987654321",
    "relacao": "Mãe"
  }
  ```
- **DELETE** `/api/contatos/<id>` - Deleta um contato

### Locais Seguros

- **GET** `/api/locais` - Lista todos os locais
- **POST** `/api/locais` - Cria novo local
  ```json
  {
    "nome": "Delegacia Centro",
    "tipo": "Delegacia",
    "endereco": "Av. Principal, 100",
    "latitude": -23.5505,
    "longitude": -46.6333
  }
  ```
- **DELETE** `/api/locais/<id>` - Deleta um local

## 🔐 Segurança (MVP)

⚠️ **Importante**: Este é um MVP. Antes de produção:

- [ ] Adicionar HTTPS
- [ ] Implementar validação forte de entrada
- [ ] Usar variáveis de ambiente para credenciais
- [ ] Adicionar rate limiting na API
- [ ] Criptografar dados sensíveis
- [ ] Testes de segurança

## 📱 Usando como PWA

1. Abra o app no navegador
2. Clique no menu (três pontos) → "Instalar app"
3. Agora funciona offline e como app nativo

## 🧪 Desenvolvimento

### Rodar em desenvolvimento
```bash
export FLASK_DEBUG=1
flask run
```

### Criar novo contato (teste)
```bash
curl -X POST http://localhost:5000/api/contatos \
  -H "Content-Type: application/json" \
  -d '{"nome": "Teste", "telefone": "11999999999", "relacao": "Amiga"}'
```

## 📝 Próximas Funcionalidades

- [ ] Histórico de localizações
- [ ] Integração com WhatsApp Business API
- [ ] Sincronização em nuvem
- [ ] Notificações de amigos
- [ ] Modo invisível
- [ ] Compartilhamento de localização em tempo real
- [ ] Autenticação de usuários

## 🤝 Contribuindo

Sugestões e contribuições são bem-vindas! Abra uma issue ou PR.

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para detalhes.

---

**Desenvolvido com ❤️ para sua segurança**
