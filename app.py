"""
App principal de segurança pessoal para mulheres.
PWA (Progressive Web App) com geolocalização e integração WhatsApp.
"""

import os
from dotenv import load_dotenv
from flask import Flask
from models import db

# Carrega variáveis de ambiente
load_dotenv()

def create_app():
    """
    Factory para criação da aplicação Flask.
    Configura banco de dados, blueprints e contextos.
    """
    app = Flask(__name__)
    
    # Configuração
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Inicializa banco de dados
    db.init_app(app)
    
    # Registra blueprints (rotas)
    from routes import main_bp, api_bp
    from routes_auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    
    # Cria tabelas no primeiro acesso
    with app.app_context():
        db.create_all()
        print('✅ Banco de dados inicializado')
    
    return app


if __name__ == '__main__':
    app = create_app()
    # Em produção, use um servidor WSGI (Gunicorn)
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    print(f'🚀 Iniciando app em http://0.0.0.0:5000 (Debug: {debug_mode})')
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
