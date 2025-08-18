from app import create_app, db
from app.models import Admin

app = create_app()
app.app_context().push()

# Criar admin padrão
admin = Admin(username='admin', email='admin@convite.com')
admin.set_password('123456')
db.session.add(admin)
db.session.commit()

print('✅ Admin criado com sucesso!')
print('👤 Usuário: admin')
print('🔑 Senha: 123456')
print('🌐 Acesse: http://localhost:5000/admin/login')
