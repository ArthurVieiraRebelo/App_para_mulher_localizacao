#!/bin/bash

# Script de inicialização para Linux/macOS
# Executa setup, limpa cache, inicia servidor

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║         🛡️  SEGURA - Iniciar Servidor                ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não está instalado"
    echo ""
    echo "Instale com:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "✓ Python 3 encontrado: $(python3 --version)"
echo ""

# Verifica se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não está instalado"
    echo ""
    echo "Instale com:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "✓ pip3 encontrado"
echo ""

# Verifica e cria arquivo .env
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "⚙️  Criando arquivo .env..."
        cp .env.example .env
        echo "✓ .env criado"
    fi
fi

# Verifica dependências
echo "📦 Verificando dependências..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependências não instaladas!"
    echo ""
    echo "Instale com:"
    echo "  pip3 install -r requirements.txt"
    exit 1
fi
echo "✓ Dependências OK"
echo ""

# Limpa cache Python
echo "🗑️  Limpando cache Python..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "✓ Cache limpo"
echo ""

# Ativa venv se existir
if [ -d venv ]; then
    echo "🔵 Ativando ambiente virtual..."
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
    echo "✓ Ambiente virtual ativo"
    echo ""
fi

# Inicia servidor Flask
echo "🚀 Iniciando servidor Flask..."
echo ""
echo "═════════════════════════════════════════════════════════"
echo ""
echo "📱 Segura está rodando em:"
echo "   http://localhost:5000"
echo ""
echo "💡 Para instalar como app PWA:"
echo "   1. Abra em um navegador do celular"
echo "   2. Menu → Instalar App (ou Add to Home Screen)"
echo ""
echo "⏹️  Pressione CTRL+C para parar o servidor"
echo ""
echo "═════════════════════════════════════════════════════════"
echo ""

python3 run.py
