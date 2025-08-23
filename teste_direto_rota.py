import requests
import json

# Teste direto na URL
url = "http://127.0.0.1:5000/admin/adicionar-presente-por-link"
data = {"link": "https://teste.com/produto"}

print("=== TESTE DIRETO DA ROTA ===")
print(f"URL: {url}")
print(f"Dados: {data}")

# Primeiro fazer login para ter sessão
session = requests.Session()

# Login
login_response = session.post("http://127.0.0.1:5000/admin/login", data={
    'username': 'admin',
    'password': 'senha123'
})

print(f"Login status: {login_response.status_code}")

# Agora testar a rota
response = session.post(url, json=data, headers={
    'Content-Type': 'application/json'
})

print(f"Status da resposta: {response.status_code}")
print(f"Headers da resposta: {dict(response.headers)}")
print(f"Primeiros 200 chars: {response.text[:200]}")

# Se for HTML, é sinal que está redirecionando ou dando erro
if "<!DOCTYPE html>" in response.text:
    print("❌ PROBLEMA: A resposta é HTML, não JSON!")
    print("Isso pode indicar redirecionamento ou erro 404/500")
else:
    print("✅ Resposta não é HTML")
    try:
        json_data = response.json()
        print(f"JSON: {json_data}")
    except:
        print("Não é JSON válido")

print("=== FIM DO TESTE ===")
