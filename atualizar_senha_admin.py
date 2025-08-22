#!/usr/bin/env python3
"""
Script para atualizar a senha do admin
"""
from app import create_app, db
from app.models import Admin

def atualizar_senha():
    app = create_app()
    with app.app_context():
        # Buscar o admin existente
        admin = Admin.query.filter_by(username='admin').first()
        
        if admin:
            # Atualizar a senha
            nova_senha = 'Casamento2025*#'
            admin.set_password(nova_senha)
            db.session.commit()
            print(f"✅ Senha do admin atualizada com sucesso!")
            print(f"🔐 Nova senha: {nova_senha}")
        else:
            print("❌ Admin não encontrado!")

if __name__ == "__main__":
    atualizar_senha()
