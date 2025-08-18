#!/usr/bin/env python3
"""
Script para corrigir sequências do PostgreSQL após migração
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Carregar variáveis de ambiente
load_dotenv()

def corrigir_sequencias():
    """Corrigir as sequências do PostgreSQL após migração"""
    
    print("🔧 CORRIGINDO SEQUÊNCIAS DO POSTGRESQL")
    print("=" * 50)
    
    database_url = os.environ.get('DATABASE_URL')
    postgres_url = database_url.replace('postgresql://', 'postgresql+pg8000://')
    engine = create_engine(postgres_url)
    
    try:
        with engine.connect() as conn:
            print("✅ Conectado ao PostgreSQL")
            
            # Corrigir sequência da tabela admin
            result = conn.execute(text("SELECT MAX(id) FROM admin"))
            max_id = result.scalar() or 0
            conn.execute(text(f"ALTER SEQUENCE admin_id_seq RESTART WITH {max_id + 1}"))
            print(f"✅ Sequência admin_id_seq ajustada para {max_id + 1}")
            
            # Corrigir sequência da tabela convidado
            result = conn.execute(text("SELECT MAX(id) FROM convidado"))
            max_id = result.scalar() or 0
            conn.execute(text(f"ALTER SEQUENCE convidado_id_seq RESTART WITH {max_id + 1}"))
            print(f"✅ Sequência convidado_id_seq ajustada para {max_id + 1}")
            
            # Corrigir sequência da tabela presente
            result = conn.execute(text("SELECT MAX(id) FROM presente"))
            max_id = result.scalar() or 0
            conn.execute(text(f"ALTER SEQUENCE presente_id_seq RESTART WITH {max_id + 1}"))
            print(f"✅ Sequência presente_id_seq ajustada para {max_id + 1}")
            
            # Corrigir sequência da tabela configuracao_site
            result = conn.execute(text("SELECT MAX(id) FROM configuracao_site"))
            max_id = result.scalar() or 0
            conn.execute(text(f"ALTER SEQUENCE configuracao_site_id_seq RESTART WITH {max_id + 1}"))
            print(f"✅ Sequência configuracao_site_id_seq ajustada para {max_id + 1}")
            
            # Corrigir sequência da tabela escolha_presente
            result = conn.execute(text("SELECT MAX(id) FROM escolha_presente"))
            max_id = result.scalar() or 0
            conn.execute(text(f"ALTER SEQUENCE escolha_presente_id_seq RESTART WITH {max_id + 1}"))
            print(f"✅ Sequência escolha_presente_id_seq ajustada para {max_id + 1}")
            
            conn.commit()
            
            print("\n🎉 Todas as sequências foram corrigidas!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    corrigir_sequencias()
