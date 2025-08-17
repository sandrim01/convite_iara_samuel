import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar extensões
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Usar SQLite para desenvolvimento se PostgreSQL não estiver disponível
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgresql://'):
        try:
            import psycopg2
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        except ImportError:
            print("⚠️  PostgreSQL não disponível, usando SQLite para desenvolvimento")
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///convite_dev.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///convite_dev.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões com app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    # Registrar blueprints
    from app.routes.main import main
    from app.routes.admin import admin
    from app.routes.convite import convite
    
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(convite, url_prefix='/convite')
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    return app
