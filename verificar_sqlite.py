#!/usr/bin/env python3
"""
Script para verificar dados no banco SQLite local
"""

import sqlite3
import os

def verificar_sqlite():
    """Verificar dados no SQLite local"""
    sqlite_path = 'instance/convite_dev.db'
    
    if not os.path.exists(sqlite_path):
        print(f"❌ Arquivo SQLite não encontrado: {sqlite_path}")
        return
    
    print(f"🔍 VERIFICANDO DADOS NO SQLITE: {sqlite_path}")
    print("=" * 60)
    
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Verificar se as tabelas existem
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = cursor.fetchall()
        
        print("📋 TABELAS ENCONTRADAS:")
        for tabela in tabelas:
            print(f"  - {tabela[0]}")
        
        print()
        
        # Verificar dados em cada tabela
        tabelas_dados = ['configuracao_site', 'admin', 'convidado', 'presente', 'escolha_presente']
        
        for tabela in tabelas_dados:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                count = cursor.fetchone()[0]
                print(f"📊 {tabela}: {count} registro(s)")
                
                if count > 0:
                    cursor.execute(f"SELECT * FROM {tabela} LIMIT 3")
                    rows = cursor.fetchall()
                    print(f"   Primeiros registros:")
                    for i, row in enumerate(rows, 1):
                        print(f"   {i}. {dict(row)}")
                    print()
                    
            except sqlite3.OperationalError as e:
                print(f"❌ Erro ao acessar tabela {tabela}: {e}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verificar_sqlite()
