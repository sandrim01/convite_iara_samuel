import requests
import json

# Configuração
base_url = "http://127.0.0.1:5000"
session = requests.Session()

print("=== TESTE COMPLETO DA API DE PRESENTES ===\n")

# 1. Login
print("1. Fazendo login...")
login_response = session.post(f"{base_url}/admin/login", data={
    'username': 'admin',
    'password': 'senha123'
})

print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    print("✅ Login realizado com sucesso")
else:
    print("❌ Falha no login")
    exit()

# 2. Verificar se conseguimos acessar a página de presentes
print("\n2. Verificando acesso à página de presentes...")
presentes_page = session.get(f"{base_url}/admin/presentes")
print(f"Página presentes status: {presentes_page.status_code}")

if presentes_page.status_code == 200:
    print("✅ Página de presentes acessível")
else:
    print("❌ Não conseguiu acessar página de presentes")

# 3. Testar a API com diferentes headers
print("\n3. Testando API com headers corretos...")

# Preparar dados
test_data = {
    "link": "https://www.americanas.com.br/produto/123456789/conjunto-panelas-tramontina"
}

# Headers que imitam a requisição do JavaScript
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
}

print(f"Enviando dados: {test_data}")
print(f"Headers: {headers}")

# Fazer a requisição
api_response = session.post(
    f"{base_url}/admin/adicionar-presente-por-link",
    json=test_data,
    headers=headers
)

print(f"\nResposta da API:")
print(f"Status: {api_response.status_code}")
print(f"Content-Type: {api_response.headers.get('content-type', 'N/A')}")
print(f"Primeira linha da resposta: {api_response.text[:100]}...")

# Verificar se é JSON
try:
    json_response = api_response.json()
    print("✅ Resposta é JSON válido:")
    print(json.dumps(json_response, indent=2, ensure_ascii=False))
except json.JSONDecodeError:
    print("❌ Resposta não é JSON válido")
    print("Conteúdo completo:")
    print(api_response.text[:500] + "..." if len(api_response.text) > 500 else api_response.text)

print("\n=== FIM DO TESTE ===")
