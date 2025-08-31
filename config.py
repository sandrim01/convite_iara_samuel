import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production-please'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # URL do PostgreSQL fornecida
    POSTGRESQL_URL = 'postgresql://postgres:WRCdYiMGmLhZfsBqFelhfOTpRCQsNIEp@tramway.proxy.rlwy.net:19242/railway'
    
    # Configuração do banco de dados
    database_url = os.environ.get('DATABASE_URL') or POSTGRESQL_URL
    
    if database_url:
        if database_url.startswith('postgresql://'):
            # Usar psycopg2 como driver
            SQLALCHEMY_DATABASE_URI = database_url.replace('postgresql://', 'postgresql+psycopg2://')
        else:
            SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Usar PostgreSQL como padrão
        SQLALCHEMY_DATABASE_URI = POSTGRESQL_URL.replace('postgresql://', 'postgresql+psycopg2://')
    
    # Configurações de conexão do PostgreSQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0,
    }

class DevelopmentConfig(Config):
    DEBUG = True
    # Usar SQLite para desenvolvimento local
    SQLALCHEMY_DATABASE_URI = 'sqlite:///convite.db'
    SQLALCHEMY_ENGINE_OPTIONS = {}

class ProductionConfig(Config):
    DEBUG = False

# Configuração baseada no ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
