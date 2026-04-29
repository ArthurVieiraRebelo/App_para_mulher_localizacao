"""
Rotas da aplicação.
Define endpoints para:
- Página principal (HTML)
- API para contatos de emergência (CRUD)
- API para locais seguros (CRUD)
"""

from flask import Blueprint, render_template, request, jsonify
from models import db, ContatoEmergencia, LocalSeguro

# Blueprint para páginas HTML
main_bp = Blueprint('main', __name__)

# Blueprint para API JSON
api_bp = Blueprint('api', __name__, url_prefix='/api')


# ==================== ROTAS PRINCIPAIS ====================

@main_bp.route('/')
def index():
    """Página inicial do app"""
    return render_template('index.html')


# ==================== API - CONTATOS DE EMERGÊNCIA ====================

@api_bp.route('/contatos', methods=['GET'])
def listar_contatos():
    """Retorna lista de todos os contatos"""
    contatos = ContatoEmergencia.query.all()
    return jsonify([c.to_dict() for c in contatos])


@api_bp.route('/contatos', methods=['POST'])
def criar_contato():
    """Cria novo contato de emergência"""
    dados = request.get_json()
    
    # Validação básica
    if not dados.get('nome') or not dados.get('telefone'):
        return jsonify({'erro': 'Nome e telefone são obrigatórios'}), 400
    
    # Remove caracteres especiais do telefone
    telefone = dados['telefone'].replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    novo_contato = ContatoEmergencia(
        nome=dados['nome'],
        telefone=telefone,
        relacao=dados.get('relacao', 'Contato')
    )
    
    db.session.add(novo_contato)
    db.session.commit()
    
    return jsonify(novo_contato.to_dict()), 201


@api_bp.route('/contatos/<int:id>', methods=['DELETE'])
def deletar_contato(id):
    """Deleta um contato de emergência"""
    contato = ContatoEmergencia.query.get_or_404(id)
    db.session.delete(contato)
    db.session.commit()
    
    return jsonify({'mensagem': 'Contato deletado'}), 200


# ==================== API - LOCAIS SEGUROS ====================

@api_bp.route('/locais', methods=['GET'])
def listar_locais():
    """Retorna lista de todos os locais seguros"""
    locais = LocalSeguro.query.all()
    return jsonify([l.to_dict() for l in locais])


@api_bp.route('/locais', methods=['POST'])
def criar_local():
    """Cria novo local seguro"""
    dados = request.get_json()
    
    # Validação
    if not dados.get('nome'):
        return jsonify({'erro': 'Nome do local é obrigatório'}), 400
    
    novo_local = LocalSeguro(
        nome=dados['nome'],
        tipo=dados.get('tipo', 'Outro'),
        latitude=dados.get('latitude'),
        longitude=dados.get('longitude'),
        endereco=dados.get('endereco')
    )
    
    db.session.add(novo_local)
    db.session.commit()
    
    return jsonify(novo_local.to_dict()), 201


@api_bp.route('/locais/<int:id>', methods=['DELETE'])
def deletar_local(id):
    """Deleta um local seguro"""
    local = LocalSeguro.query.get_or_404(id)
    db.session.delete(local)
    db.session.commit()
    
    return jsonify({'mensagem': 'Local deletado'}), 200


# ==================== HELPER ====================

@api_bp.route('/localizacao', methods=['POST'])
def salvar_localizacao():
    """
    Endpoint para salvar localização (futuro log de histórico).
    Recebe latitude e longitude do frontend.
    """
    dados = request.get_json()
    lat = dados.get('latitude')
    lon = dados.get('longitude')
    
    # Por enquanto apenas confirma recebimento
    # Depois podemos salvar em um histórico
    return jsonify({
        'sucesso': True,
        'mensagem': f'Localização recebida: {lat}, {lon}'
    }), 200
