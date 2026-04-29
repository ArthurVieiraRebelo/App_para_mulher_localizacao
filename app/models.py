"""
Modelos de banco de dados para o app de segurança pessoal.
Define as tabelas: Contatos de Emergência e Locais Seguros
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class ContatoEmergencia(db.Model):
    """
    Modelo para contatos de emergência.
    Armazena nome, telefone e relacionamento.
    """
    __tablename__ = 'contatos_emergencia'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    relacao = db.Column(db.String(50), default='Contato')  # mãe, amiga, etc.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContatoEmergencia {self.nome}>'
    
    def to_dict(self):
        """Converte o objeto para dicionário (útil para JSON)"""
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'relacao': self.relacao
        }


class LocalSeguro(db.Model):
    """
    Modelo para locais seguros (delegacias, hospitais, amigos, etc).
    Armazena nome, coordenadas e tipo de local.
    """
    __tablename__ = 'locais_seguros'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(50), default='Outro')  # Delegacia, Hospital, Amigo, etc.
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    endereco = db.Column(db.String(200), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LocalSeguro {self.nome}>'
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'endereco': self.endereco
        }
