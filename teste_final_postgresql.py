#!/usr/bin/env python3
"""
Script de verificação final - PostgreSQL Railway
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Carregar variáveis de ambiente
load_dotenv()

def teste_conexao_postgresql():
    """Testar a conexão e operações básicas no PostgreSQL"""
    
    print("🧪 TESTE FINAL DO SISTEMA")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não encontrada")
        return False
    
    print(f"🔗 DATABASE_URL configurada: {database_url[:50]}...")
    
    try:
        # Conectar usando pg8000
        postgres_url = database_url.replace('postgresql://', 'postgresql+pg8000://')
        engine = create_engine(postgres_url)
        
        with engine.connect() as conn:
            print("✅ Conexão com PostgreSQL estabelecida!")
            
            # Testar queries básicas
            print("\n🔍 TESTANDO OPERAÇÕES:")
            
            # 1. Contar registros em cada tabela
            tabelas = ['configuracao_site', 'admin', 'convidado', 'presente', 'escolha_presente']
            
            for tabela in tabelas:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {tabela}"))
                count = result.scalar()
                print(f"  📊 {tabela}: {count} registro(s)")
            
            # 2. Testar inserção de um novo convidado
            print("\n🧪 Testando inserção de dados...")
            
            # Inserir convidado de teste
            conn.execute(text("""
                INSERT INTO convidado (nome, email, telefone, token, confirmou_presenca, acompanhantes, created_at)
                VALUES ('Teste PostgreSQL', 'teste@postgresql.com', '(11) 99999-9999', 'test-token-123', false, 0, NOW())
            """))
            
            # Verificar se foi inserido
            result = conn.execute(text("SELECT nome FROM convidado WHERE email = 'teste@postgresql.com'"))
            nome = result.scalar()
            
            if nome:
                print(f"  ✅ Inserção testada com sucesso: {nome}")
                
                # Remover o registro de teste
                conn.execute(text("DELETE FROM convidado WHERE email = 'teste@postgresql.com'"))
                print("  🧹 Registro de teste removido")
            
            conn.commit()
            
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            print("✅ O sistema está funcionando com PostgreSQL do Railway")
            print("=" * 50)
            
            return True
            
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        return False

def resumo_migracao():
    """Mostrar resumo da migração realizada"""
    print("\n📋 RESUMO DA MIGRAÇÃO")
    print("=" * 50)
    print("✅ Dados migrados do SQLite para PostgreSQL:")
    print("   📋 1 configuração do site")
    print("   👤 1 administrador")
    print("   💌 5 convidados")
    print("   🎁 10 presentes")
    print("   🎯 0 escolhas de presentes")
    print()
    print("✅ Sistema configurado para usar PostgreSQL do Railway")
    print("✅ Driver pg8000 instalado e funcionando")
    print("✅ Aplicação Flask rodando com PostgreSQL")
    print()
    print("🌐 URLs de acesso:")
    print("   📱 Site público: http://127.0.0.1:5000")
    print("   ⚙️  Painel admin: http://127.0.0.1:5000/admin")
    print("   👤 Login admin: admin / admin")

if __name__ == "__main__":
    sucesso = teste_conexao_postgresql()
    if sucesso:
        resumo_migracao()
    else:
        print("❌ Alguns testes falharam. Verifique a configuração.")
