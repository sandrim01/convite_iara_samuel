import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, login_manager
from flask_migrate import Migrate

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
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    # Registrar blueprints
    from app.routes.main import main
    from app.routes.admin import admin
    # from app.routes.convite import convite
    
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    # app.register_blueprint(convite, url_prefix='/convite')
    
    # Filtros personalizados para templates
    @app.template_filter('safe_currency')
    def safe_currency_filter(value):
        """Filtro seguro para formatação de moeda"""
        try:
            if value is None or value == '':
                return 'R$ 0,00'
            return f'R$ {float(value):.2f}'
        except (ValueError, TypeError):
            return 'R$ 0,00'
    
    @app.template_filter('safe_sum')
    def safe_sum_filter(items, attribute):
        """Filtro seguro para soma de atributos"""
        try:
            total = 0
            for item in items:
                value = getattr(item, attribute, None)
                if value is not None:
                    total += float(value)
            return total
        except (ValueError, TypeError):
            return 0
    
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
            admin_user.set_password('Casamento2025*#')
            db.session.add(admin_user)
            db.session.commit()
            print("👤 Admin padrão criado: admin/Casamento2025*#")
    
    return app
