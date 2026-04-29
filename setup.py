"""
Script de inicialização e setup do projeto.
Execute isto para preparar tudo para desenvolvimento.
"""

import os
import sys
from pathlib import Path

def limpar_cache():
    """Remove arquivos de cache Python"""
    print('\n🗑️  Limpando cache Python...')
    
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache = os.path.join(root, '__pycache__')
            import shutil
            shutil.rmtree(pycache)
            print(f'  ✓ Removido {pycache}')
        
        for arquivo in files:
            if arquivo.endswith('.pyc'):
                os.remove(os.path.join(root, arquivo))

def criar_env():
    """Cria arquivo .env se não existir"""
    print('\n⚙️  Configurando variáveis de ambiente...')
    
    if os.path.exists('.env'):
        print('  ✓ .env já existe')
        return
    
    # Cria .env a partir do .env.example
    if os.path.exists('.env.example'):
        import shutil
        shutil.copy('.env.example', '.env')
        print('  ✓ .env criado a partir de .env.example')
    else:
        print('  ⚠️  .env.example não encontrado')

def criar_banco():
    """Inicializa banco de dados"""
    print('\n🗄️  Inicializando banco de dados...')
    
    from app import create_app
    from models import db
    
    app = create_app()
    with app.app_context():
        db.create_all()
        print('  ✓ Banco de dados criado com sucesso')

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print('\n📦 Verificando dependências...')
    
    try:
        import flask
        print('  ✓ Flask')
        import flask_sqlalchemy
        print('  ✓ Flask-SQLAlchemy')
        import sqlalchemy
        print('  ✓ SQLAlchemy')
        import dotenv
        print('  ✓ python-dotenv')
        import requests
        print('  ✓ requests')
        return True
    except ImportError as e:
        print(f'  ❌ Falta: {e}')
        return False

def gerar_icones():
    """Gera ícones para PWA"""
    print('\n🎨 Gerando ícones PWA...')
    
    try:
        from gerar_icones import gerar_icones as gerar
        gerar('static')
        print('  ✓ Ícones gerados')
    except Exception as e:
        print(f'  ⚠️  Erro ao gerar ícones: {e}')

def main():
    print('''
╔════════════════════════════════════════════════════════╗
║                                                        ║
║         🛡️  SETUP - SEGURA (Segurança Pessoal)       ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
    ''')
    
    # 1. Verifica dependências
    if not verificar_dependencias():
        print('\n❌ Instale as dependências primeiro:')
        print('   pip install -r requirements.txt')
        return
    
    # 2. Cria .env
    criar_env()
    
    # 3. Cria banco de dados
    try:
        criar_banco()
    except Exception as e:
        print(f'  ❌ Erro ao criar banco: {e}')
        return
    
    # 4. Gera ícones
    gerar_icones()
    
    # 5. Limpa cache
    limpar_cache()
    
    print('\n' + '='*56)
    print('✅ Setup concluído com sucesso!')
    print('='*56)
    
    print('\n🚀 Para iniciar o servidor, execute:')
    print('   python app.py')
    
    print('\n📍 App estará disponível em:')
    print('   http://localhost:5000')
    
    print('\n📱 Para testar como PWA:')
    print('   1. Abra no navegador do celular')
    print('   2. Menu → "Instalar app" ou "Add to Home Screen"')
    
    print('\n💡 Próximos passos:')
    print('   1. Configure WhatsApp Business API (ver WHATSAPP_SETUP.md)')
    print('   2. Cadastre contatos de emergência')
    print('   3. Adicione locais seguros')
    print('   4. Teste o botão de pânico')
    
    print('\n📚 Documentação:')
    print('   - README.md: Visão geral')
    print('   - WHATSAPP_SETUP.md: Integração WhatsApp')
    print('   - routes_auth.py: Sistema de autenticação')
    
    print('\n' + '='*56 + '\n')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n❌ Setup cancelado pelo usuário')
    except Exception as e:
        print(f'\n❌ Erro durante setup: {e}')
        import traceback
        traceback.print_exc()
