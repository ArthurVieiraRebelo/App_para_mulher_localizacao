"""
Pacote principal da aplicação Segura.
Exporta os principais módulos e componentes.
"""

from flask_sqlalchemy import SQLAlchemy

# Instância global do banco de dados
db = SQLAlchemy()

# Importa modelos
from app.models import ContatoEmergencia, LocalSeguro
from app.models_avancados import Usuario, HistoricoSOS

__all__ = ['db', 'ContatoEmergencia', 'LocalSeguro', 'Usuario', 'HistoricoSOS']
