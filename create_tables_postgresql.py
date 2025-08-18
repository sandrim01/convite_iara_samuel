#!/usr/bin/env python3
"""
Script direto para criar tabelas no PostgreSQL usando SQLAlchemy
"""

import os
from sqlalchemy import create_engine, text

# URL do banco fornecida (modificada para pg8000)
DATABASE_URL = "postgresql+pg8000://postgres:WRCdYiMGmLhZfsBqFelhfOTpRCQsNIEp@tramway.proxy.rlwy.net:19242/railway"

def create_tables():
    """Cria todas as tabelas necessárias"""
    try:
        print("🔗 Conectando ao PostgreSQL...")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            print("✅ Conexão estabelecida!")
            
            # Criar tabela admin
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS admin (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            print("✅ Tabela 'admin' criada")
            
            # Criar tabela configuracao_site
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS configuracao_site (
                    id SERIAL PRIMARY KEY,
                    nome_noivo VARCHAR(100) DEFAULT 'Samuel',
                    nome_noiva VARCHAR(100) DEFAULT 'Iara',
                    data_casamento DATE,
                    local_cerimonia TEXT,
                    endereco_cerimonia TEXT,
                    horario_cerimonia TIME,
                    local_festa TEXT,
                    endereco_festa TEXT,
                    horario_festa TIME,
                    mensagem_principal TEXT,
                    cor_tema VARCHAR(7) DEFAULT '#d4a574',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            print("✅ Tabela 'configuracao_site' criada")
            
            # Criar tabela convidado
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS convidado (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(120),
                    telefone VARCHAR(20),
                    token VARCHAR(100) UNIQUE NOT NULL DEFAULT gen_random_uuid()::text,
                    confirmou_presenca BOOLEAN DEFAULT FALSE,
                    data_confirmacao TIMESTAMP,
                    acompanhantes INTEGER DEFAULT 0,
                    observacoes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            print("✅ Tabela 'convidado' criada")
            
            # Criar tabela presente
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS presente (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(200) NOT NULL,
                    descricao TEXT,
                    categoria VARCHAR(50),
                    preco_sugerido DECIMAL(10,2),
                    link_loja VARCHAR(500),
                    imagem_url VARCHAR(500),
                    disponivel BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            print("✅ Tabela 'presente' criada")
            
            # Criar tabela escolha_presente
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS escolha_presente (
                    id SERIAL PRIMARY KEY,
                    convidado_id INTEGER REFERENCES convidado(id),
                    presente_id INTEGER REFERENCES presente(id),
                    data_escolha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    entregue BOOLEAN DEFAULT FALSE,
                    data_entrega TIMESTAMP,
                    observacoes TEXT
                );
            """))
            print("✅ Tabela 'escolha_presente' criada")
            
            conn.commit()
            
        print("\n🎉 Todas as tabelas foram criadas com sucesso!")
        print(f"📊 Banco: tramway.proxy.rlwy.net:19242/railway")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    create_tables()
