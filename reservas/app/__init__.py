from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Inicialización de extensiones
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuración básica
    app.config['SECRET_KEY'] = 'clave_super_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel_reservas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar base de datos y login
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Importar y registrar blueprints
    from app.auth_routes import auth_bp
    from app.booking_routes import booking_bp
    from app.payment_routes import payment_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(payment_bp)

    # Crear base de datos si no existe
    with app.app_context():
        if not os.path.exists('hotel_reservas.db'):
            db.create_all()

    return app
