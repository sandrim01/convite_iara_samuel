import requests
import json

session = requests.Session()

print("=== TESTE COM SENHA CORRETA ===")

# 1. Login com a senha correta
print("1. Fazendo login com senha correta...")
login_response = session.post("http://127.0.0.1:5000/admin/login", data={
    'username': 'admin',
    'password': 'Casamento2025*#'
})
print(f"Login status: {login_response.status_code}")

# 2. Verificar se consegue acessar dashboard
print("\n2. Testando acesso ao dashboard...")
dashboard_response = session.get("http://127.0.0.1:5000/admin/dashboard")
print(f"Dashboard status: {dashboard_response.status_code}")

# 3. Testar a API de adicionar presente
print("\n3. Testando API de adicionar presente...")
api_response = session.post("http://127.0.0.1:5000/admin/adicionar-presente-por-link", 
                           json={"link": "https://www.americanas.com.br/produto/teste"})

print(f"API status: {api_response.status_code}")
print(f"Content-Type: {api_response.headers.get('content-type')}")

if api_response.text.startswith('<!DOCTYPE html>'):
    print("❌ Ainda retornando HTML")
    # Verificar título
    import re
    title_match = re.search(r'<title>(.*?)</title>', api_response.text)
    if title_match:
        print(f"Título: {title_match.group(1)}")
else:
    try:
        json_data = api_response.json()
        print("✅ Resposta JSON:")
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
    except:
        print(f"Resposta de texto: {api_response.text[:200]}")

print("=== FIM DO TESTE ===")
