#!/usr/bin/env python3
"""
Script para migrar o banco de dados e adicionar campos do WhatsApp
"""

import os
import sys
from sqlalchemy import text

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from config import Config

def migrar_whatsapp():
    """Adiciona colunas para controle de envio do WhatsApp"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 Iniciando migração para WhatsApp...")
            
            # Verificar se as colunas já existem
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'convidado' 
                AND column_name IN ('convite_enviado_whatsapp', 'data_envio_whatsapp')
            """))
            
            existing_columns = [row[0] for row in result]
            
            # Adicionar coluna convite_enviado_whatsapp se não existir
            if 'convite_enviado_whatsapp' not in existing_columns:
                print("➕ Adicionando coluna 'convite_enviado_whatsapp'...")
                db.session.execute(text("""
                    ALTER TABLE convidado 
                    ADD COLUMN convite_enviado_whatsapp BOOLEAN DEFAULT FALSE
                """))
                print("✅ Coluna 'convite_enviado_whatsapp' adicionada com sucesso!")
            else:
                print("ℹ️  Coluna 'convite_enviado_whatsapp' já existe")
            
            # Adicionar coluna data_envio_whatsapp se não existir
            if 'data_envio_whatsapp' not in existing_columns:
                print("➕ Adicionando coluna 'data_envio_whatsapp'...")
                db.session.execute(text("""
                    ALTER TABLE convidado 
                    ADD COLUMN data_envio_whatsapp TIMESTAMP NULL
                """))
                print("✅ Coluna 'data_envio_whatsapp' adicionada com sucesso!")
            else:
                print("ℹ️  Coluna 'data_envio_whatsapp' já existe")
            
            # Commit das alterações
            db.session.commit()
            
            print("🎉 Migração concluída com sucesso!")
            print("📱 Sistema de WhatsApp está pronto para uso!")
            
            # Verificar quantos convidados estão prontos para receber convite
            from app.models import Convidado
            liberados = Convidado.query.filter_by(liberado_recepcao=True).count()
            com_telefone = Convidado.query.filter(
                Convidado.liberado_recepcao == True,
                Convidado.telefone.isnot(None),
                Convidado.telefone != ''
            ).count()
            
            print(f"📊 Estatísticas:")
            print(f"   • {liberados} convidados liberados para recepção")
            print(f"   • {com_telefone} convidados com telefone cadastrado")
            print(f"   • {liberados - com_telefone} convidados sem telefone")
            
        except Exception as e:
            print(f"❌ Erro durante a migração: {str(e)}")
            db.session.rollback()
            return False
            
    return True

if __name__ == "__main__":
    print("🚀 Executando migração do WhatsApp...")
    print("=" * 50)
    
    success = migrar_whatsapp()
    
    if success:
        print("=" * 50)
        print("✅ Migração executada com sucesso!")
        print("🔗 Acesse /admin/convidados para usar o sistema WhatsApp")
    else:
        print("=" * 50)
        print("❌ Migração falhou!")
        sys.exit(1)
