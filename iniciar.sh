#!/bin/bash

# Script de inicialização rápida para Linux/Mac
# Executa: setup.py + app.py

cat << "EOF"

╔════════════════════════════════════════════════════════╗
║                                                        ║
║    🛡️  INICIAR APP - SEGURA (Linux/Mac)             ║
║                                                        ║
╚════════════════════════════════════════════════════════╝

EOF

# 1. Verifica se venv existe
if [ ! -d "venv" ]; then
    echo "⏳ Criando ambiente virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar venv"
        exit 1
    fi
fi

# 2. Ativa venv
echo "⏳ Ativando ambiente virtual..."
source venv/bin/activate

# 3. Instala dependências
echo "⏳ Instalando dependências..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

# 4. Executa setup
echo "⏳ Executando setup..."
python setup.py
if [ $? -ne 0 ]; then
    echo "❌ Erro durante setup"
    exit 1
fi

# 5. Inicia app
echo ""
echo "✅ Iniciando app..."
echo ""

python app.py
