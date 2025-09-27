import os

class Config:
    
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'SUPER_SECRET_KEY_DO_FLASK')
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'SUPER_SECRET_KEY_PARA_O_JWT')
    
    MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1') 
    MYSQL_USER = os.environ.get('MYSQL_USER', 'flask_user')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'senha') 
    MYSQL_DB = os.environ.get('MYSQL_DB', 'aiqfome_favoritos')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
