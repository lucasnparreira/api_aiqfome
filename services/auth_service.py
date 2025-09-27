from extensions import db, bcrypt, get_db_cursor 
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError 

class AuthService:
    
    @staticmethod
    def hash_password(password):
        """Gera o hash da senha."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def check_password(hashed_password, password):
        """Verifica se a senha fornecida corresponde ao hash."""
        return bcrypt.check_password_hash(hashed_password, password)

    @staticmethod
    def register_client(nome, email, password):
        """
        Cria um novo cliente no banco de dados.
        Retorna o ID do cliente ou None se o e-mail já existir.
        """
        hashed_pw = AuthService.hash_password(password)
        cursor = get_db_cursor() 
        
        try:
            query = "INSERT INTO clientes (nome, email, senha) VALUES (%s, %s, %s)"
            cursor.execute(query, (nome, email, hashed_pw))
            cursor.connection.commit() 
            return cursor.lastrowid
        
        except IntegrityError:
            return None 
            
        finally:
            cursor.close()

    @staticmethod
    def authenticate_client(email, password):
        """
        Autentica o cliente.
        Retorna o token JWT e o ID do cliente ou None, None em caso de falha.
        """
        cursor = get_db_cursor()
        query = "SELECT id, senha FROM clientes WHERE email = %s"
        cursor.execute(query, [email])
        client_data = cursor.fetchone()
        cursor.close()
        
        if client_data:
            client_id, hashed_pw = client_data
            if AuthService.check_password(hashed_pw, password):
                access_token = create_access_token(identity=client_id)
                return access_token, client_id
        
        return None, None
