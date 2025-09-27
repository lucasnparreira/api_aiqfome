from flask import Flask
from config import Config
from extensions import db, jwt, bcrypt 
from sqlalchemy.exc import IntegrityError 
from extensions import get_db_cursor 

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)

from routes.auth_routes import auth_bp
from routes.cliente_routes import cliente_bp
from routes.favorito_routes import favorito_bp

app.register_blueprint(auth_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(favorito_bp)

if __name__ == '__main__':
    app.run(debug=True)
