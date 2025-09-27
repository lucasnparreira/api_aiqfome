from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.favorito_service import FavoritoService

favorito_bp = Blueprint('favorito', __name__, url_prefix='/favoritos')

@favorito_bp.route('/', methods=['POST'])
@jwt_required()
def add_favorite():
    """Adiciona um produto à lista de favoritos do cliente autenticado."""
    cliente_id = get_jwt_identity()
    data = request.get_json()
    produto_id = data.get('produto_id')
    
    if not isinstance(produto_id, int) or produto_id <= 0:
        return jsonify({"msg": "ID de produto inválido ou ausente."}), 400

    result = FavoritoService.add_favorite(cliente_id, produto_id)
    
    if result is True:
        return jsonify({"msg": f"Produto ID {produto_id} adicionado aos favoritos com sucesso."}), 201
    elif result == "Conflict":
        return jsonify({"msg": f"Produto ID {produto_id} já está na sua lista de favoritos."}), 409
    elif result == "NotFound":
        return jsonify({"msg": f"Produto ID {produto_id} não encontrado na API externa. Não pode ser favoritado."}), 404
    else:
        return jsonify({"msg": "Erro interno ao processar a requisição de favorito."}), 500

@favorito_bp.route('/', methods=['GET'])
@jwt_required()
def list_favorites():
    """Lista todos os produtos favoritos do cliente autenticado, buscando detalhes externos."""
    cliente_id = get_jwt_identity()
    
    favorites_list = FavoritoService.get_client_favorites(cliente_id)
    
    if favorites_list is False:
        return jsonify({"msg": "Erro ao comunicar com a API de produtos. Tente novamente mais tarde."}), 503 

    return jsonify(favorites_list), 200

@favorito_bp.route('/<int:produto_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(produto_id):
    """Remove um produto específico da lista de favoritos do cliente autenticado."""
    cliente_id = get_jwt_identity()
    
    if FavoritoService.remove_favorite(cliente_id, produto_id):
        return jsonify({"msg": f"Produto ID {produto_id} removido da lista de favoritos."}), 200
    else:
        return jsonify({"msg": f"Produto ID {produto_id} não encontrado na sua lista de favoritos."}), 404