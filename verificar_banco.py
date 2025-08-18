from app import create_app, db
from app.models import ConfiguracaoSite, Admin, Convidado, Presente
import os

app = create_app()
app.app_context().push()

print("🗄️  VERIFICANDO BANCO DE DADOS EXISTENTE")
print("=" * 50)

# Verificar configuração do site
print("\n📋 CONFIGURAÇÃO DO SITE:")
config = ConfiguracaoSite.query.first()
if config:
    print(f"  👰 Noiva: {config.nome_noiva}")
    print(f"  🤵 Noivo: {config.nome_noivo}")
    print(f"  📅 Data: {config.data_casamento}")
    print(f"  ⛪ Local Cerimônia: {config.local_cerimonia}")
    print(f"  🎉 Local Festa: {config.local_festa}")
    print(f"  💌 Mensagem: {config.mensagem_principal}")
else:
    print("  ❌ Nenhuma configuração encontrada")

# Verificar administradores
print("\n👥 ADMINISTRADORES:")
admins = Admin.query.all()
for admin in admins:
    print(f"  👤 {admin.username} - {admin.email}")

# Verificar convidados
print("\n💌 CONVIDADOS:")
convidados = Convidado.query.all()
if convidados:
    for convidado in convidados:
        status = "✅ Confirmado" if convidado.confirmou_presenca else "⏳ Pendente"
        print(f"  {convidado.nome} - {convidado.email} - {status}")
    print(f"\nTotal: {len(convidados)} convidados")
else:
    print("  ❌ Nenhum convidado encontrado")

# Verificar presentes
print("\n🎁 PRESENTES:")
presentes = Presente.query.all()
if presentes:
    for presente in presentes:
        status = "✅ Disponível" if presente.disponivel else "❌ Indisponível"
        preco = f"R$ {presente.preco_sugerido:.2f}" if presente.preco_sugerido else "Sem preço"
        print(f"  {presente.nome} - {presente.categoria} - {preco} - {status}")
    print(f"\nTotal: {len(presentes)} presentes")
else:
    print("  ❌ Nenhum presente encontrado")

print("\n" + "=" * 50)
print("✅ Verificação completa!")
