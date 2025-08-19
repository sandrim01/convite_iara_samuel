from app import create_app, db
from app.models import Admin

# Criar a aplicação
app = create_app()

with app.app_context():
    # Verificar todos os admins
    admins = Admin.query.all()
    
    if admins:
        print(f"📋 Encontrados {len(admins)} usuários admin:")
        for admin in admins:
            print(f"  - ID: {admin.id}")
            print(f"    Username: {admin.username}")
            print(f"    Email: {admin.email}")
            print(f"    Criado em: {admin.created_at}")
            print("---")
    else:
        print("❌ Nenhum usuário admin encontrado!")
        print("🔧 Criando admin padrão...")
        
        # Criar admin padrão
        admin_user = Admin(
            username='admin',
            email='admin@convite.com'
        )
        admin_user.set_password('admin')
        db.session.add(admin_user)
        db.session.commit()
        
        print("✅ Admin padrão criado: admin/admin")
