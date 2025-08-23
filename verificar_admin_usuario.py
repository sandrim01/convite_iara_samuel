from app import create_app
from app.models import Admin

app = create_app()

print("=== VERIFICAÇÃO DO USUÁRIO ADMIN ===")

with app.app_context():
    # Listar todos os usuários admin
    admins = Admin.query.all()
    print(f"Total de admins: {len(admins)}")
    
    for admin in admins:
        print(f"ID: {admin.id}, Username: {admin.username}")
        
        # Testar se a senha 'senha123' funciona
        if admin.check_password('senha123'):
            print(f"✅ Senha 'senha123' é válida para {admin.username}")
        else:
            print(f"❌ Senha 'senha123' não é válida para {admin.username}")
    
    # Verificar especificamente o usuário 'admin'
    admin_user = Admin.query.filter_by(username='admin').first()
    if admin_user:
        print(f"\n✅ Usuário 'admin' encontrado (ID: {admin_user.id})")
        print(f"Password hash: {admin_user.password_hash[:20]}...")
    else:
        print("\n❌ Usuário 'admin' não encontrado!")
        
print("=== FIM DA VERIFICAÇÃO ===")
