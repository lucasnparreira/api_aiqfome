from extensions import db, bcrypt, get_db_cursor 
from services.auth_service import AuthService
from sqlalchemy.exc import IntegrityError 

class ClienteService:

    @staticmethod
    def get_client_by_id(client_id):
        """Busca um cliente pelo ID (sem retornar a senha)."""
        cursor = get_db_cursor()
        query = "SELECT id, nome, email, data_cadastro FROM clientes WHERE id = %s"
        cursor.execute(query, [client_id])
        client = cursor.fetchone()
        cursor.close()
        
        if client:
            return {
                "id": client[0],
                "nome": client[1],
                "email": client[2],
                "data_cadastro": client[3]
            }
        return None

    @staticmethod
    def update_client(client_id, data):
        """Atualiza nome e/ou e-mail de um cliente."""
        cursor = get_db_cursor()
        
        set_parts = []
        params = []
        
        if 'nome' in data:
            set_parts.append("nome = %s")
            params.append(data['nome'])
        
        if 'email' in data:
            set_parts.append("email = %s")
            params.append(data['email'])

        if not set_parts:
            cursor.close()
            return True

        query = "UPDATE clientes SET " + ", ".join(set_parts) + " WHERE id = %s"
        params.append(client_id)
        
        try:
            cursor.execute(query, params)
            cursor.connection.commit() 
            return cursor.rowcount > 0
        
        except IntegrityError: 
            return "EmailConflict" 
            
        finally:
            cursor.close()
            
    @staticmethod
    def delete_client(client_id):
        """Remove um cliente pelo ID."""
        cursor = get_db_cursor()
        query = "DELETE FROM clientes WHERE id = %s"
        cursor.execute(query, [client_id])
        cursor.connection.commit() 
        
        return cursor.rowcount > 0 
