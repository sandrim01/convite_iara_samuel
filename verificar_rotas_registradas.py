from app import create_app

# Criar app
app = create_app()

print("=== ROTAS REGISTRADAS ===")
with app.app_context():
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods - {'OPTIONS', 'HEAD'})
        print(f"{rule.endpoint:30} {methods:15} {rule.rule}")

print("\n=== PROCURANDO ROTA ESPECÍFICA ===")
target_route = "/admin/adicionar-presente-por-link"
found = False

with app.app_context():
    for rule in app.url_map.iter_rules():
        if rule.rule == target_route:
            print(f"✅ ENCONTRADA: {rule.endpoint} - Métodos: {rule.methods}")
            found = True

if not found:
    print(f"❌ ROTA {target_route} NÃO ENCONTRADA!")
    print("\nRotas admin disponíveis:")
    with app.app_context():
        for rule in app.url_map.iter_rules():
            if rule.rule.startswith('/admin'):
                print(f"  {rule.rule}")
