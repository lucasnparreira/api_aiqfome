from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.cliente_service import ClienteService

cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes')

@cliente_bp.route('/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
    """Visualiza os dados de um cliente."""
    current_client_id = get_jwt_identity()
    
    if client_id != current_client_id:
        return jsonify({"msg": "Acesso negado: Você só pode visualizar seu próprio perfil."}), 403

    client = ClienteService.get_client_by_id(client_id)
    
    if client:
        return jsonify(client), 200
    else:
        return jsonify({"msg": "Cliente não encontrado."}), 404

@cliente_bp.route('/<int:client_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_client(client_id):
    """Edita os dados de um cliente (nome ou email)."""
    current_client_id = get_jwt_identity()
    data = request.get_json()
    
    if client_id != current_client_id:
        return jsonify({"msg": "Acesso negado: Você só pode editar seu próprio perfil."}), 403
    
    allowed_fields = {'nome', 'email'}
    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_data:
        return jsonify({"msg": "Nenhum campo válido para atualização fornecido (apenas nome e email)."}), 400

    result = ClienteService.update_client(client_id, update_data)
    
    if result == "EmailConflict":
        return jsonify({"msg": "Falha na atualização: O e-mail fornecido já está em uso."}), 409
    
    if result:
        return jsonify({"msg": "Perfil atualizado com sucesso!"}), 200
    else:
        return jsonify({"msg": "Cliente não encontrado ou nenhum dado alterado."}), 404

@cliente_bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    """Remove a conta do cliente."""
    current_client_id = get_jwt_identity()
    
    if client_id != current_client_id:
        return jsonify({"msg": "Acesso negado: Você só pode deletar sua própria conta."}), 403
    
    if ClienteService.delete_client(client_id):
        return jsonify({"msg": "Conta deletada com sucesso. Todos os seus favoritos foram removidos."}), 200
    else:
        return jsonify({"msg": "Cliente não encontrado."}), 404