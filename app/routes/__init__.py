"""Blueprints da aplicacao."""

from app.routes.auth import auth_bp
from app.routes.main import api_bp, main_bp

__all__ = ['main_bp', 'api_bp', 'auth_bp']
