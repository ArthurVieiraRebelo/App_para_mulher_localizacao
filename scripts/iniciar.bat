@echo off
REM Script de inicialização rápida para Windows
REM Executa setup, limpa cache, inicia servidor

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║         🛡️  SEGURA - Iniciar Servidor (Windows)      ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não está instalado ou não está no PATH
    echo.
    echo Para instalar:
    echo   1. Baixe em: https://www.python.org/downloads/
    echo   2. Marque "Add Python to PATH" durante instalação
    pause
    exit /b 1
)

echo ✓ Python encontrado
echo.

REM Verifica e cria arquivo .env
if not exist .env (
    if exist .env.example (
        echo ⚙️  Criando arquivo .env...
        copy .env.example .env >nul
        echo ✓ .env criado
    )
)

REM Verifica dependências
echo 📦 Verificando dependências...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo ❌ Dependências não instaladas!
    echo.
    echo Instale com:
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✓ Dependências OK
echo.

REM Executa setup (opcional, comentado por padrão)
REM echo 🔧 Executando setup...
REM python scripts\setup.py
REM echo.

REM Limpa cache Python
echo 🗑️  Limpando cache...
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" rmdir /s /q "%%d"
)
echo ✓ Cache limpo
echo.

REM Inicia servidor Flask
echo 🚀 Iniciando servidor Flask...
echo.
echo ═════════════════════════════════════════════════════════
echo.
echo 📱 Segura está rodando em:
echo    http://localhost:5000
echo.
echo 💡 Para instalar como app PWA:
echo    1. Abra em um navegador do celular
echo    2. Menu → Instalar App (ou Add to Home Screen)
echo.
echo ⏹️  Pressione CTRL+C para parar o servidor
echo.
echo ═════════════════════════════════════════════════════════
echo.

python run.py

pause
