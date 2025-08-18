import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, login_manager

# Carregar variáveis de ambiente
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Configuração do banco PostgreSQL
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgresql://'):
        # Usar pg8000 como driver PostgreSQL
        postgres_url = database_url.replace('postgresql://', 'postgresql+pg8000://')
        app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url
        print("🐘 Conectando ao PostgreSQL usando pg8000...")
    else:
        # Fallback para SQLite em desenvolvimento
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///convite.db'
        print("📂 Usando SQLite para desenvolvimento...")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
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
    
    # Importar modelos e criar tabelas
    with app.app_context():
        from app.models import Admin, ConfiguracaoSite, Convidado, Presente, EscolhaPresente
        db.create_all()
        
        # Criar admin padrão se não existir
        if not Admin.query.first():
            admin_user = Admin(
                username='admin',
                email='admin@convite.com'
            )
            admin_user.set_password('admin')
            db.session.add(admin_user)
            db.session.commit()
            print("👤 Admin padrão criado: admin/admin")
    
    return app
