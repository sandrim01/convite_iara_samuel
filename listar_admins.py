from app import create_app, db
from app.models import Admin

app = create_app()
app.app_context().push()

# Verificar admins existentes
admins = Admin.query.all()

if admins:
    print('👥 Administradores encontrados:')
    for admin in admins:
        print(f'  👤 Usuário: {admin.username}')
        print(f'  📧 Email: {admin.email}')
        print(f'  📅 Criado em: {admin.created_at}')
        print('  ─────────────────────')
else:
    print('❌ Nenhum administrador encontrado')
