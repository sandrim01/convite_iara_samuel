#!/usr/bin/env python3
"""
Script para adicionar o campo liberado_recepcao à tabela de convidados
"""

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models import Convidado

def main():
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar se a coluna já existe
            inspector = db.inspect(db.engine)
            columns = [column['name'] for column in inspector.get_columns('convidado')]
            
            if 'liberado_recepcao' not in columns:
                print("Adicionando coluna 'liberado_recepcao' à tabela convidado...")
                
                # Adicionar a coluna
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE convidado ADD COLUMN liberado_recepcao BOOLEAN DEFAULT FALSE'))
                    
                    # Atualizar convidados que já confirmaram presença
                    conn.execute(db.text('''
                        UPDATE convidado 
                        SET liberado_recepcao = TRUE 
                        WHERE confirmacao = TRUE
                    '''))
                    conn.commit()
                
                print("✅ Coluna adicionada com sucesso!")
                print("✅ Convidados que já confirmaram foram automaticamente liberados para recepção!")
            else:
                print("ℹ️  Coluna 'liberado_recepcao' já existe.")
                
        except Exception as e:
            print(f"❌ Erro ao executar migração: {e}")
            return False
            
    return True

if __name__ == '__main__':
    if main():
        print("\n🎉 Migração concluída com sucesso!")
    else:
        print("\n💥 Falha na migração!")
        sys.exit(1)
