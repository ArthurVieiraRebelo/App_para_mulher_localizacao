"""Modelos e instancia do banco de dados."""

from app.models.base import ContatoEmergencia, LocalSeguro, db
from app.models.advanced import HistoricoSOS, Usuario

__all__ = ['db', 'ContatoEmergencia', 'LocalSeguro', 'Usuario', 'HistoricoSOS']
