"""Pacote principal da aplicacao Segura."""

from app.models import ContatoEmergencia, HistoricoSOS, LocalSeguro, Usuario, db

__all__ = ['db', 'ContatoEmergencia', 'LocalSeguro', 'Usuario', 'HistoricoSOS']
