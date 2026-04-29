"""
Modelos adicionados para funcionalidades avançadas:
- Histórico de SOS
- Usuários com autenticação básica
"""

from models import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    """
    Modelo para usuários do app.
    Autenticação simples com email e senha.
    """
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(100), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    contatos = db.relationship('ContatoEmergencia', backref='usuario', lazy=True, cascade='all, delete-orphan')
    locais = db.relationship('LocalSeguro', backref='usuario', lazy=True, cascade='all, delete-orphan')
    historico_sos = db.relationship('HistoricoSOS', backref='usuario', lazy=True, cascade='all, delete-orphan')
    
    def set_senha(self, senha):
        """Hash a senha de forma segura"""
        self.senha_hash = generate_password_hash(senha, method='pbkdf2:sha256')
    
    def check_senha(self, senha):
        """Verifica se a senha está correta"""
        return check_password_hash(self.senha_hash, senha)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nome': self.nome,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat()
        }


class HistoricoSOS(db.Model):
    """
    Registra cada acionamento do botão SOS.
    Útil para análise e rastreamento.
    """
    __tablename__ = 'historico_sos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Contato para quem foi enviado
    contato_id = db.Column(db.Integer, db.ForeignKey('contatos_emergencia.id'), nullable=True)
    contato_nome = db.Column(db.String(100), nullable=True)  # Snapshot do nome
    contato_telefone = db.Column(db.String(20), nullable=True)  # Snapshot do telefone
    
    # Status
    status = db.Column(db.String(20), default='enviado')  # enviado, confirmado, fechado
    motivo = db.Column(db.String(500), nullable=True)  # Opcional: por que acionou
    
    # Data e hora
    acionado_em = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<HistoricoSOS {self.id} - {self.acionado_em}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'contato_nome': self.contato_nome,
            'contato_telefone': self.contato_telefone,
            'status': self.status,
            'motivo': self.motivo,
            'acionado_em': self.acionado_em.isoformat()
        }
