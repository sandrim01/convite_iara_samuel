"""
Script para criar usuário administrador 'master'
"""

import sys
import os

# Adicionar o diretório da aplicação ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, Admin

def criar_usuario_master():
    """Cria usuário administrador 'master'"""
    
    app = create_app()
    
    with app.app_context():
        print("👤 Criando usuário administrador 'master'...")
        
        # Verificar se já existe
        existing_user = Admin.query.filter_by(username='master').first()
        
        if existing_user:
            print("⚠️  Usuário 'master' já existe!")
            print("🔄 Atualizando senha...")
            existing_user.set_password('master123')
            db.session.commit()
            print("✅ Senha do usuário 'master' atualizada!")
        else:
            print("➕ Criando novo usuário 'master'...")
            
            # Criar novo admin
            master = Admin(username='master', email='master@casamento.com')
            master.set_password('master123')
            
            db.session.add(master)
            db.session.commit()
            
            print("✅ Usuário 'master' criado com sucesso!")
        
        print("\n📋 Credenciais do usuário 'master':")
        print("   - Usuário: master")
        print("   - Senha: master123")
        
        # Listar todos os admins para confirmar
        print("\n👥 Todos os administradores:")
        admins = Admin.query.all()
        for admin in admins:
            print(f"   - {admin.username}")

if __name__ == "__main__":
    criar_usuario_master()
