import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, login_manager

# Carregar variáveis de ambiente
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Determinar ambiente
    env = os.environ.get('FLASK_ENV', 'development')
    if os.environ.get('RAILWAY_ENVIRONMENT_NAME'):
        env = 'production'
    
    # Configurações baseadas no ambiente
    if env == 'production':
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
        print("🚀 Rodando em modo PRODUÇÃO...")
    else:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
        print("� Rodando em modo DESENVOLVIMENTO...")
    
    # Log da configuração do banco
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if 'postgresql' in db_uri:
        print("🐘 Conectando ao PostgreSQL...")
    else:
        print("📂 Usando SQLite para desenvolvimento...")
    
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
