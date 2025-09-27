import requests
from extensions import db, get_db_cursor 
from flask import jsonify
from sqlalchemy.exc import IntegrityError 

FAKE_STORE_API_BASE = "https://fakestoreapi.com"

class FavoritoService:

    @staticmethod
    def get_product_details(product_id):
        """Busca e valida os detalhes de um produto na API Externa."""
        try:
            url = f"{FAKE_STORE_API_BASE}/products/{product_id}"
            response = requests.get(url, timeout=5) 
            
            if response.status_code == 200:
                data = response.json()
            
                if 'id' in data and data['id'] == product_id:
                    return {
                        "id": data.get('id'),
                        "titulo": data.get('title'),
                        "imagem": data.get('image'),
                        "preco": data.get('price'),
                        "review": data.get('rating', {}).get('rate', 'N/A') 
                    }
                return None 
                
            elif response.status_code == 404:
                return None 

            else:
                print(f"Erro na Fake Store API: Status {response.status_code}")
                return False 

        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão com API externa: {e}")
            return False

    @staticmethod
    def add_favorite(cliente_id, produto_id):
        """
        Adiciona um produto à lista de favoritos do cliente.
        Retorna: True (sucesso), "NotFound" (produto inválido), "Conflict" (duplicado), ou False (erro DB).
        """

        product_details = FavoritoService.get_product_details(produto_id)
        
        if product_details is None:
            return "NotFound" 
        
        if product_details is False:
            return False 

        cursor = get_db_cursor()
        try:
            query = "INSERT INTO favoritos (cliente_id, produto_id) VALUES (%s, %s)"
            cursor.execute(query, (cliente_id, produto_id))
            cursor.connection.commit() 
            return True
            
        except IntegrityError: 
            return "Conflict" 
            
        except Exception as e:
            print(f"Erro ao inserir favorito no DB: {e}")
            return False 
            
        finally:
            cursor.close()

    @staticmethod
    def get_client_favorites(cliente_id):
        """Lista os IDs de todos os produtos favoritos de um cliente."""
        cursor = get_db_cursor()
        query = "SELECT produto_id FROM favoritos WHERE cliente_id = %s"
        cursor.execute(query, [cliente_id])
        
        favorite_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        
        favorite_products = []
        for p_id in favorite_ids:
            details = FavoritoService.get_product_details(p_id)
            if details:
                favorite_products.append(details)
            
        return favorite_products

    @staticmethod
    def remove_favorite(cliente_id, produto_id):
        """Remove um produto da lista de favoritos do cliente."""
        cursor = get_db_cursor()
        query = "DELETE FROM favoritos WHERE cliente_id = %s AND produto_id = %s"
        cursor.execute(query, (cliente_id, produto_id))
        cursor.connection.commit() 
        
        return cursor.rowcount > 0
