import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production-please'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração do banco de dados
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgresql://'):
            # Corrigir URL do PostgreSQL para usar pg8000
            SQLALCHEMY_DATABASE_URI = database_url.replace('postgresql://', 'postgresql+pg8000://')
        else:
            SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Fallback para SQLite em desenvolvimento
        SQLALCHEMY_DATABASE_URI = 'sqlite:///convite.db'
    
    # Configurações de produção
    if os.environ.get('RAILWAY_ENVIRONMENT_NAME'):
        # Estamos no Railway
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
        }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///convite.db'

class ProductionConfig(Config):
    DEBUG = False

# Configuração baseada no ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
