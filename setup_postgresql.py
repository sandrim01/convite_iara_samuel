#!/usr/bin/env python3
"""
Script para criar todas as tabelas necessárias no PostgreSQL
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app import create_app, db
from app.models import Admin, Convidado, Presente, EscolhaPresente, ConfiguracaoSite
from datetime import datetime, date

def test_connection():
    """Testa a conexão com o PostgreSQL"""
    try:
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL não encontrada no .env")
            return False
            
        print(f"🔗 Testando conexão com: {database_url.split('@')[1]}")
        
        # Conectar usando psycopg2 diretamente
        conn = psycopg2.connect(database_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL conectado: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def create_tables():
    """Cria todas as tabelas usando SQLAlchemy"""
    try:
        print("\n🏗️  Criando aplicação Flask...")
        app = create_app()
        
        with app.app_context():
            print("🗃️  Criando todas as tabelas...")
            
            # Primeiro, vamos tentar dropar e recriar tudo
            db.drop_all()
            print("🧹 Tabelas existentes removidas")
            
            # Criar todas as tabelas
            db.create_all()
            print("✅ Todas as tabelas criadas com sucesso!")
            
            # Verificar quais tabelas foram criadas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Tabelas criadas: {', '.join(tables)}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False

def populate_initial_data():
    """Popula dados iniciais necessários"""
    try:
        app = create_app()
        
        with app.app_context():
            print("\n📊 Populando dados iniciais...")
            
            # Criar admin padrão
            admin_existente = Admin.query.filter_by(username='admin').first()
            if not admin_existente:
                admin = Admin(
                    username='admin',
                    email='admin@convite.com'
                )
                admin.set_password('123456')
                db.session.add(admin)
                print("👤 Admin criado: admin / 123456")
            else:
                print("👤 Admin já existe")
            
            # Criar configuração inicial
            config_existente = ConfiguracaoSite.query.first()
            if not config_existente:
                config = ConfiguracaoSite(
                    nome_noiva='Iara',
                    nome_noivo='Samuel',
                    data_casamento=date(2025, 11, 28),
                    local_cerimonia='Igreja São Francisco de Assis',
                    endereco_cerimonia='Rua das Flores, 123 - Centro, São Paulo - SP',
                    horario_cerimonia=datetime.strptime("16:00", "%H:%M").time(),
                    local_festa='Espaço Jardim Encantado',
                    endereco_festa='Av. Paulista, 456 - Bela Vista, São Paulo - SP',
                    horario_festa=datetime.strptime("18:00", "%H:%M").time(),
                    mensagem_principal='Criamos esse site para compartilhar com vocês os detalhes da organização do nosso casamento. ♥'
                )
                db.session.add(config)
                print("⚙️  Configuração inicial criada")
            else:
                print("⚙️  Configuração já existe")
            
            # Adicionar alguns presentes de exemplo
            presentes_exemplo = [
                {
                    "nome": "Jogo de Panelas Antiaderente",
                    "categoria": "Cozinha",
                    "descricao": "Conjunto com 5 panelas antiaderentes de alta qualidade",
                    "preco_sugerido": 299.90,
                    "link_loja": "https://www.magazineluiza.com.br/panelas"
                },
                {
                    "nome": "Jogo de Cama Casal King",
                    "categoria": "Quarto",
                    "descricao": "Jogo de cama 100% algodão, 300 fios",
                    "preco_sugerido": 189.90,
                    "link_loja": "https://www.casasbahia.com.br/jogo-cama"
                },
                {
                    "nome": "Cafeteira Elétrica",
                    "categoria": "Eletrodomésticos",
                    "descricao": "Cafeteira elétrica programável para 12 xícaras",
                    "preco_sugerido": 159.90,
                    "link_loja": "https://www.americanas.com.br/cafeteira"
                },
                {
                    "nome": "Conjunto de Taças de Cristal",
                    "categoria": "Mesa",
                    "descricao": "6 taças de cristal para vinho e champagne",
                    "preco_sugerido": 249.90,
                    "link_loja": "https://www.submarino.com.br/tacas"
                },
                {
                    "nome": "Aspirador de Pó Robot",
                    "categoria": "Limpeza",
                    "descricao": "Aspirador robô inteligente com mapeamento",
                    "preco_sugerido": 899.90,
                    "link_loja": "https://www.amazon.com.br/aspirador"
                }
            ]
            
            for presente_data in presentes_exemplo:
                presente_existente = Presente.query.filter_by(nome=presente_data["nome"]).first()
                if not presente_existente:
                    presente = Presente(**presente_data)
                    db.session.add(presente)
            
            print("🎁 Presentes de exemplo adicionados")
            
            # Adicionar alguns convidados de exemplo
            convidados_exemplo = [
                {"nome": "Maria Silva", "email": "maria@email.com", "telefone": "(11) 99999-1111"},
                {"nome": "João Santos", "email": "joao@email.com", "telefone": "(11) 99999-2222"},
                {"nome": "Ana Costa", "email": "ana@email.com", "telefone": "(11) 99999-3333"}
            ]
            
            for conv_data in convidados_exemplo:
                convidado_existente = Convidado.query.filter_by(email=conv_data["email"]).first()
                if not convidado_existente:
                    convidado = Convidado(**conv_data)
                    db.session.add(convidado)
            
            print("💌 Convidados de exemplo adicionados")
            
            # Salvar tudo
            db.session.commit()
            print("✅ Dados iniciais salvos com sucesso!")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao popular dados: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 CONFIGURANDO POSTGRESQL NO RAILWAY")
    print("=" * 50)
    
    # Testar conexão
    if not test_connection():
        print("❌ Falha na conexão. Verifique a DATABASE_URL")
        return
    
    # Criar tabelas
    if not create_tables():
        print("❌ Falha ao criar tabelas")
        return
    
    # Popular dados iniciais
    if not populate_initial_data():
        print("❌ Falha ao popular dados iniciais")
        return
    
    print("\n" + "=" * 50)
    print("🎉 POSTGRESQL CONFIGURADO COM SUCESSO!")
    print("\n📋 INFORMAÇÕES:")
    print("👤 Admin: admin / 123456")
    print("📧 Email: admin@convite.com")
    print("🌐 URL: http://localhost:5000/admin/login")
    print("📅 Data do Casamento: 28/11/2025")
    print("🎁 Presentes: 5 exemplos criados")
    print("💌 Convidados: 3 exemplos criados")

if __name__ == "__main__":
    main()
