"""
Script para verificar e criar usuário administrador se necessário
"""

import sys
import os

# Adicionar o diretório da aplicação ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, Admin

def verificar_admin():
    """Verifica se existe usuário admin e cria se necessário"""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Verificando usuários administradores...")
        
        # Listar todos os admins
        admins = Admin.query.all()
        
        if admins:
            print(f"📋 Encontrados {len(admins)} administrador(es):")
            for admin in admins:
                print(f"   - Usuário: {admin.username}")
        else:
            print("❌ Nenhum administrador encontrado!")
            print("➕ Criando administrador padrão...")
            
            # Criar admin padrão
            admin = Admin(username='admin')
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Administrador criado:")
            print("   - Usuário: admin")
            print("   - Senha: admin123")

if __name__ == "__main__":
    verificar_admin()
