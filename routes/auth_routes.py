from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint para registrar um novo cliente."""
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')

    if not all([nome, email, password]):
        return jsonify({"msg": "Nome, e-mail e senha são obrigatórios"}), 400
    
    client_id = AuthService.register_client(nome, email, password)
    
    if client_id is None:
        return jsonify({"msg": "E-mail já cadastrado."}), 409 
    
    return jsonify({
        "msg": "Cliente registrado com sucesso.",
        "client_id": client_id
    }), 201 

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para autenticar e gerar o token JWT."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({"msg": "E-mail e senha são obrigatórios"}), 400
    
    token, client_id = AuthService.authenticate_client(email, password)
    
    if token:
        return jsonify({
            "msg": "Login bem-sucedido.",
            "access_token": token
        }), 200
    else:
        return jsonify({"msg": "E-mail ou senha inválidos."}), 401