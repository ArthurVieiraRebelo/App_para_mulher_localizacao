#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de teste interativo para validar todas as funcionalidades.
Execute: python test_app.py
"""

import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000'

class Cores:
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    RESET = '\033[0m'

def print_titulo(titulo):
    print(f'\n{Cores.AZUL}{"="*60}{Cores.RESET}')
    print(f'{Cores.AZUL}{titulo:^60}{Cores.RESET}')
    print(f'{Cores.AZUL}{"="*60}{Cores.RESET}\n')

def print_sucesso(msg):
    print(f'{Cores.VERDE}✓ {msg}{Cores.RESET}')

def print_erro(msg):
    print(f'{Cores.VERMELHO}✗ {msg}{Cores.RESET}')

def print_info(msg):
    print(f'{Cores.AZUL}ℹ {msg}{Cores.RESET}')

def print_aviso(msg):
    print(f'{Cores.AMARELO}⚠ {msg}{Cores.RESET}')

def testar_conexao():
    """Testa se o servidor está rodando"""
    print_titulo('1. TESTE DE CONEXÃO')
    
    try:
        response = requests.get(f'{BASE_URL}/', timeout=5)
        if response.status_code == 200:
            print_sucesso('Servidor está rodando em http://localhost:5000')
            return True
        else:
            print_erro(f'Status inesperado: {response.status_code}')
            return False
    except requests.ConnectionError:
        print_erro('Servidor não está respondendo!')
        print_info('Execute: python app.py')
        return False
    except Exception as e:
        print_erro(f'Erro: {e}')
        return False

def testar_registro():
    """Testa registro de novo usuário"""
    print_titulo('2. TESTE DE REGISTRO')
    
    email = f'teste_{datetime.now().timestamp()}@exemplo.com'
    dados = {
        'nome': 'Usuária Teste',
        'email': email,
        'senha': 'senha123456'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/auth/registro',
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 201:
            print_sucesso(f'Usuário criado: {email}')
            print_info(f'Resposta: {response.json()}')
            return email, dados['senha']
        else:
            print_erro(f'Erro: {response.status_code}')
            print_info(f'Resposta: {response.json()}')
            return None, None
            
    except Exception as e:
        print_erro(f'Erro na requisição: {e}')
        return None, None

def testar_login(email, senha):
    """Testa login de usuário"""
    print_titulo('3. TESTE DE LOGIN')
    
    dados = {
        'email': email,
        'senha': senha
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/auth/login',
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            print_sucesso(f'Login realizado para {email}')
            print_info(f'Resposta: {response.json()}')
            return True
        else:
            print_erro(f'Erro no login: {response.status_code}')
            print_info(f'Resposta: {response.json()}')
            return False
            
    except Exception as e:
        print_erro(f'Erro na requisição: {e}')
        return False

def testar_contatos():
    """Testa CRUD de contatos"""
    print_titulo('4. TESTE DE CONTATOS')
    
    # Criar contato
    novo_contato = {
        'nome': 'Maria Silva',
        'telefone': '(21) 98765-4321',
        'relacao': 'Mãe'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/contatos',
            json=novo_contato,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 201:
            print_sucesso('Contato criado com sucesso')
            contato = response.json()
            print_info(f'ID: {contato["id"]}, Nome: {contato["nome"]}')
            
            # Listar contatos
            response = requests.get(f'{BASE_URL}/api/contatos', timeout=5)
            if response.status_code == 200:
                contatos = response.json()
                print_sucesso(f'Total de contatos: {len(contatos)}')
                for c in contatos:
                    print_info(f'  - {c["nome"]} ({c["telefone"]})')
                return True
        else:
            print_erro(f'Erro ao criar contato: {response.status_code}')
            return False
            
    except Exception as e:
        print_erro(f'Erro na requisição: {e}')
        return False

def testar_locais():
    """Testa CRUD de locais seguros"""
    print_titulo('5. TESTE DE LOCAIS SEGUROS')
    
    novo_local = {
        'nome': 'Delegacia Centro',
        'tipo': 'Delegacia',
        'endereco': 'Av. Principal, 100',
        'latitude': -23.5505,
        'longitude': -46.6333
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/locais',
            json=novo_local,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 201:
            print_sucesso('Local criado com sucesso')
            local = response.json()
            print_info(f'ID: {local["id"]}, Nome: {local["nome"]}')
            
            # Listar locais
            response = requests.get(f'{BASE_URL}/api/locais', timeout=5)
            if response.status_code == 200:
                locais = response.json()
                print_sucesso(f'Total de locais: {len(locais)}')
                for l in locais:
                    print_info(f'  - {l["nome"]} ({l["tipo"]})')
                return True
        else:
            print_erro(f'Erro ao criar local: {response.status_code}')
            return False
            
    except Exception as e:
        print_erro(f'Erro na requisição: {e}')
        return False

def testar_geoloc():
    """Testa endpoint de geolocalização"""
    print_titulo('6. TESTE DE GEOLOCALIZAÇÃO')
    
    dados = {
        'latitude': -23.5505,
        'longitude': -46.6333
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/localizacao',
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            print_sucesso('Localização recebida com sucesso')
            print_info(f'Resposta: {response.json()}')
            return True
        else:
            print_erro(f'Erro ao enviar localização: {response.status_code}')
            return False
            
    except Exception as e:
        print_erro(f'Erro na requisição: {e}')
        return False

def testar_pwa():
    """Testa se PWA está configurado"""
    print_titulo('7. TESTE DE PWA')
    
    try:
        # Testa manifest
        response = requests.get(f'{BASE_URL}/static/manifest.json', timeout=5)
        if response.status_code == 200:
            print_sucesso('manifest.json encontrado')
            manifest = response.json()
            print_info(f'  - Nome: {manifest.get("name")}')
            print_info(f'  - Display: {manifest.get("display")}')
        else:
            print_aviso('manifest.json não encontrado')
        
        # Testa service worker
        response = requests.get(f'{BASE_URL}/static/js/sw.js', timeout=5)
        if response.status_code == 200:
            print_sucesso('Service Worker encontrado')
        else:
            print_aviso('Service Worker não encontrado')
        
        return True
        
    except Exception as e:
        print_erro(f'Erro: {e}')
        return False

def main():
    print(f'''
    
╔════════════════════════════════════════════════════════╗
║                                                        ║
║    🛡️  TESTES - SEGURA (Segurança Pessoal)           ║
║                                                        ║
║  Valida todas as funcionalidades implementadas       ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
    ''')
    
    # 1. Conexão
    if not testar_conexao():
        return
    
    # 2. Registro
    email, senha = testar_registro()
    if not email:
        print_aviso('Pulando testes de login (falha no registro)')
        return
    
    # 3. Login
    if not testar_login(email, senha):
        print_aviso('Pulando testes (falha no login)')
        return
    
    # 4. Contatos
    testar_contatos()
    
    # 5. Locais
    testar_locais()
    
    # 6. Geolocalização
    testar_geoloc()
    
    # 7. PWA
    testar_pwa()
    
    # Resumo final
    print_titulo('✅ TESTES CONCLUÍDOS')
    print_sucesso('Todas as funcionalidades foram testadas!')
    print_info('Próximos passos:')
    print_info('  1. Abra http://localhost:5000 no navegador')
    print_info('  2. Teste o botão de pânico')
    print_info('  3. Configure WhatsApp Business API')
    print_info('  4. Teste em celular real')
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n\n{Cores.AMARELO}Testes cancelados pelo usuário{Cores.RESET}\n')
    except Exception as e:
        print(f'\n\n{Cores.VERMELHO}Erro durante testes: {e}{Cores.RESET}\n')
        import traceback
        traceback.print_exc()
