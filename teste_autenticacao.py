import requests

session = requests.Session()

print("=== TESTE DE AUTENTICAÇÃO ===")

# 1. Tentar acessar rota protegida sem login
print("1. Testando sem login...")
response = session.post("http://127.0.0.1:5000/admin/adicionar-presente-por-link", 
                       json={"link": "teste"})
print(f"Sem login - Status: {response.status_code}")
print(f"Sem login - É HTML: {'<!DOCTYPE html>' in response.text}")

# 2. Fazer login
print("\n2. Fazendo login...")
login_response = session.post("http://127.0.0.1:5000/admin/login", data={
    'username': 'admin',
    'password': 'senha123'
})
print(f"Login status: {login_response.status_code}")
print(f"Cookies após login: {list(session.cookies.keys())}")

# 3. Verificar se consegue acessar uma página admin simples
print("\n3. Testando acesso à página admin...")
admin_page = session.get("http://127.0.0.1:5000/admin/dashboard")
print(f"Dashboard status: {admin_page.status_code}")
print(f"Dashboard é HTML: {'<!DOCTYPE html>' in admin_page.text}")
print(f"Dashboard tem 'dashboard' no texto: {'dashboard' in admin_page.text.lower()}")

# 4. Agora tentar a rota POST novamente
print("\n4. Testando rota POST após login...")
response = session.post("http://127.0.0.1:5000/admin/adicionar-presente-por-link", 
                       json={"link": "teste"})
print(f"Com login - Status: {response.status_code}")
print(f"Com login - É HTML: {'<!DOCTYPE html>' in response.text}")

# 5. Verificar conteúdo da resposta
if '<!DOCTYPE html>' in response.text:
    print("\n5. Analisando conteúdo HTML...")
    if 'login' in response.text.lower():
        print("❌ Parece que está redirecionando para login")
    elif 'dashboard' in response.text.lower():
        print("❌ Parece que está redirecionando para dashboard")
    elif 'presentes' in response.text.lower():
        print("❌ Parece que está redirecionando para página de presentes")
    else:
        print("❌ Redirecionando para página desconhecida")
        
    # Buscar por título na página
    import re
    title_match = re.search(r'<title>(.*?)</title>', response.text)
    if title_match:
        print(f"Título da página: {title_match.group(1)}")

print("=== FIM DO TESTE ===")
