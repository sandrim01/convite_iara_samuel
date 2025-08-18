#!/usr/bin/env python3
"""
Script para migrar dados do SQLite local para PostgreSQL do Railway
"""

import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Carregar variáveis de ambiente
load_dotenv()

def conectar_sqlite():
    """Conectar ao banco SQLite local"""
    sqlite_path = 'instance/convite_dev.db'
    if not os.path.exists(sqlite_path):
        print(f"❌ Arquivo SQLite não encontrado: {sqlite_path}")
        return None
    
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
    return conn

def conectar_postgresql():
    """Conectar ao PostgreSQL do Railway"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não encontrada no .env")
        return None
    
    # Usar pg8000 como driver
    postgres_url = database_url.replace('postgresql://', 'postgresql+pg8000://')
    engine = create_engine(postgres_url)
    return engine

def migrar_dados():
    """Migrar todos os dados do SQLite para PostgreSQL"""
    
    print("🔄 INICIANDO MIGRAÇÃO DE DADOS")
    print("=" * 50)
    
    # Conectar aos bancos
    sqlite_conn = conectar_sqlite()
    if not sqlite_conn:
        return False
    
    pg_engine = conectar_postgresql()
    if not pg_engine:
        return False
    
    try:
        with pg_engine.connect() as pg_conn:
            # Obter cursor SQLite
            sqlite_cursor = sqlite_conn.cursor()
            
            # 1. Migrar configuração do site
            print("📋 Migrando configuração do site...")
            sqlite_cursor.execute("SELECT * FROM configuracao_site")
            config_rows = sqlite_cursor.fetchall()
            
            for row in config_rows:
                pg_conn.execute(text("""
                    INSERT INTO configuracao_site (
                        nome_noiva, nome_noivo, data_casamento, local_cerimonia,
                        endereco_cerimonia, horario_cerimonia, local_festa, endereco_festa,
                        horario_festa, mensagem_principal, cor_tema, updated_at
                    ) VALUES (
                        :nome_noiva, :nome_noivo, :data_casamento, :local_cerimonia,
                        :endereco_cerimonia, :horario_cerimonia, :local_festa, :endereco_festa,
                        :horario_festa, :mensagem_principal, :cor_tema, :updated_at
                    )
                """), {
                    'nome_noiva': row['nome_noiva'],
                    'nome_noivo': row['nome_noivo'],
                    'data_casamento': row['data_casamento'],
                    'local_cerimonia': row['local_cerimonia'],
                    'endereco_cerimonia': row['endereco_cerimonia'],
                    'horario_cerimonia': row['horario_cerimonia'],
                    'local_festa': row['local_festa'],
                    'endereco_festa': row['endereco_festa'],
                    'horario_festa': row['horario_festa'],
                    'mensagem_principal': row['mensagem_principal'],
                    'cor_tema': row['cor_tema'],
                    'updated_at': row['updated_at']
                })
            print(f"✅ {len(config_rows)} configuração(ões) migrada(s)")
            
            # 2. Migrar administradores
            print("👤 Migrando administradores...")
            sqlite_cursor.execute("SELECT * FROM admin")
            admin_rows = sqlite_cursor.fetchall()
            
            for row in admin_rows:
                pg_conn.execute(text("""
                    INSERT INTO admin (
                        id, username, email, password_hash, created_at
                    ) VALUES (
                        :id, :username, :email, :password_hash, :created_at
                    )
                """), {
                    'id': row['id'],
                    'username': row['username'],
                    'email': row['email'],
                    'password_hash': row['password_hash'],
                    'created_at': row['created_at']
                })
            print(f"✅ {len(admin_rows)} administrador(es) migrado(s)")
            
            # 3. Migrar convidados
            print("💌 Migrando convidados...")
            sqlite_cursor.execute("SELECT * FROM convidado")
            convidado_rows = sqlite_cursor.fetchall()
            
            for row in convidado_rows:
                pg_conn.execute(text("""
                    INSERT INTO convidado (
                        id, nome, email, telefone, token, confirmou_presenca,
                        data_confirmacao, acompanhantes, observacoes, created_at
                    ) VALUES (
                        :id, :nome, :email, :telefone, :token, :confirmou_presenca,
                        :data_confirmacao, :acompanhantes, :observacoes, :created_at
                    )
                """), {
                    'id': row['id'],
                    'nome': row['nome'],
                    'email': row['email'],
                    'telefone': row['telefone'],
                    'token': row['token'],
                    'confirmou_presenca': bool(row['confirmou_presenca']),
                    'data_confirmacao': row['data_confirmacao'],
                    'acompanhantes': row['acompanhantes'],
                    'observacoes': row['observacoes'],
                    'created_at': row['created_at']
                })
            print(f"✅ {len(convidado_rows)} convidado(s) migrado(s)")
            
            # 4. Migrar presentes
            print("🎁 Migrando presentes...")
            sqlite_cursor.execute("SELECT * FROM presente")
            presente_rows = sqlite_cursor.fetchall()
            
            for row in presente_rows:
                pg_conn.execute(text("""
                    INSERT INTO presente (
                        id, nome, descricao, categoria, preco_sugerido, link_loja,
                        imagem_url, disponivel, created_at
                    ) VALUES (
                        :id, :nome, :descricao, :categoria, :preco_sugerido, :link_loja,
                        :imagem_url, :disponivel, :created_at
                    )
                """), {
                    'id': row['id'],
                    'nome': row['nome'],
                    'descricao': row['descricao'],
                    'categoria': row['categoria'],
                    'preco_sugerido': row['preco_sugerido'],
                    'link_loja': row['link_loja'],
                    'imagem_url': row['imagem_url'],
                    'disponivel': bool(row['disponivel']),
                    'created_at': row['created_at']
                })
            print(f"✅ {len(presente_rows)} presente(s) migrado(s)")
            
            # 5. Migrar escolhas de presentes
            print("🎯 Migrando escolhas de presentes...")
            sqlite_cursor.execute("SELECT * FROM escolha_presente")
            escolha_rows = sqlite_cursor.fetchall()
            
            for row in escolha_rows:
                pg_conn.execute(text("""
                    INSERT INTO escolha_presente (
                        id, convidado_id, presente_id, data_escolha
                    ) VALUES (
                        :id, :convidado_id, :presente_id, :data_escolha
                    )
                """), {
                    'id': row['id'],
                    'convidado_id': row['convidado_id'],
                    'presente_id': row['presente_id'],
                    'data_escolha': row['data_escolha']
                })
            print(f"✅ {len(escolha_rows)} escolha(s) de presente migrada(s)")
            
            # Commit das alterações
            pg_conn.commit()
            
        print("\n🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
        return False
        
    finally:
        sqlite_conn.close()

if __name__ == "__main__":
    migrar_dados()
