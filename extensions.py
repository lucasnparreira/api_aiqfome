from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def get_db_cursor():
    """Retorna o cursor de conexão com o MySQL através do SQLAlchemy engine."""

    if db.engine:
        return db.engine.raw_connection().cursor()
    return None
