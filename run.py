#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Entry point principal da aplicação Segura.
Ponto de partida para executar o app.

Uso:
    python run.py
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Factory function para criar e retornar app
def create_app():
    """
    Factory para criação da aplicação Flask.
    Configura banco de dados, blueprints e contextos.
    """
    from flask import Flask
    from app.models import db
    
    app = Flask(__name__)
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Configuração
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Inicializa banco de dados
    db.init_app(app)
    
    # Registra blueprints (rotas)
    from app.routes import main_bp, api_bp
    from app.routes_auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    
    # Cria tabelas no primeiro acesso
    with app.app_context():
        db.create_all()
        print('Banco de dados inicializado')
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Configurações
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f'\n{'='*60}')
    print('APP SEGURA - Seguranca Pessoal para Mulheres')
    print(f'{'='*60}')
    print(f'Iniciando servidor em http://{host}:{port}')
    print(f'Debug: {debug_mode}')
    print(f'Banco: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    print(f'{'='*60}\n')
    
    # Em produção, use um servidor WSGI (Gunicorn)
    app.run(debug=debug_mode, host=host, port=port)
