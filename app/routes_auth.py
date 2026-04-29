"""
Rotas de autenticação e gerenciamento de usuários.
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from app.models import db, ContatoEmergencia, LocalSeguro
from app.models_avancados import Usuario, HistoricoSOS

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_requerido(f):
    """Decorador para rotas que exigem login"""
    @wraps(f)
    def decorado(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorado


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registra novo usuário"""
    if request.method == 'GET':
        return render_template('auth/registro.html')
    
    dados = request.get_json()
    
    # Validação
    if not dados.get('email') or not dados.get('senha'):
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
    
    if len(dados['senha']) < 6:
        return jsonify({'erro': 'Senha deve ter no mínimo 6 caracteres'}), 400
    
    # Verifica se usuário já existe
    if Usuario.query.filter_by(email=dados['email']).first():
        return jsonify({'erro': 'Email já cadastrado'}), 409
    
    # Cria novo usuário
    novo_usuario = Usuario(
        email=dados['email'],
        nome=dados.get('nome', 'Usuária')
    )
    novo_usuario.set_senha(dados['senha'])
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    # Faz login automático
    session['usuario_id'] = novo_usuario.id
    session['usuario_nome'] = novo_usuario.nome
    
    return jsonify({'sucesso': True, 'mensagem': 'Conta criada com sucesso'}), 201


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Faz login de usuário"""
    if request.method == 'GET':
        if 'usuario_id' in session:
            return redirect(url_for('main.index'))
        return render_template('auth/login.html')
    
    dados = request.get_json()
    
    # Validação
    if not dados.get('email') or not dados.get('senha'):
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
    
    # Busca usuário
    usuario = Usuario.query.filter_by(email=dados['email']).first()
    
    if not usuario or not usuario.check_senha(dados['senha']):
        return jsonify({'erro': 'Email ou senha incorretos'}), 401
    
    # Login bem-sucedido
    session['usuario_id'] = usuario.id
    session['usuario_nome'] = usuario.nome
    
    return jsonify({'sucesso': True, 'mensagem': 'Login realizado'}), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Faz logout do usuário"""
    session.clear()
    return jsonify({'sucesso': True, 'mensagem': 'Logout realizado'}), 200


@auth_bp.route('/perfil', methods=['GET'])
@login_requerido
def perfil():
    """Retorna dados do usuário logado"""
    usuario = Usuario.query.get(session['usuario_id'])
    
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    return jsonify(usuario.to_dict()), 200


# ==================== HISTÓRICO SOS ====================

@auth_bp.route('/historico-sos', methods=['GET'])
@login_requerido
def listar_historico_sos():
    """Lista histórico de SOS do usuário"""
    usuario_id = session['usuario_id']
    
    # Paginação
    pagina = request.args.get('pagina', 1, type=int)
    limite = request.args.get('limite', 20, type=int)
    
    historico = HistoricoSOS.query.filter_by(usuario_id=usuario_id)\
        .order_by(HistoricoSOS.acionado_em.desc())\
        .paginate(page=pagina, per_page=limite)
    
    return jsonify({
        'total': historico.total,
        'paginas': historico.pages,
        'pagina_atual': pagina,
        'items': [item.to_dict() for item in historico.items]
    }), 200


@auth_bp.route('/historico-sos', methods=['POST'])
@login_requerido
def registrar_sos():
    """Registra novo acionamento de SOS"""
    usuario_id = session['usuario_id']
    dados = request.get_json()
    
    novo_sos = HistoricoSOS(
        usuario_id=usuario_id,
        latitude=dados.get('latitude'),
        longitude=dados.get('longitude'),
        contato_id=dados.get('contato_id'),
        contato_nome=dados.get('contato_nome'),
        contato_telefone=dados.get('contato_telefone'),
        motivo=dados.get('motivo')
    )
    
    db.session.add(novo_sos)
    db.session.commit()
    
    return jsonify({
        'sucesso': True,
        'id': novo_sos.id,
        'mensagem': 'SOS registrado'
    }), 201


@auth_bp.route('/historico-sos/<int:id>', methods=['PATCH'])
@login_requerido
def atualizar_status_sos(id):
    """Atualiza status de um SOS"""
    usuario_id = session['usuario_id']
    sos = HistoricoSOS.query.filter_by(id=id, usuario_id=usuario_id).first_or_404()
    
    dados = request.get_json()
    
    if 'status' in dados:
        sos.status = dados['status']
    
    db.session.commit()
    
    return jsonify(sos.to_dict()), 200
