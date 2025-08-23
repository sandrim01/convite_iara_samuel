import requests
import time

# Configurar sessão
session = requests.Session()

print("=== TESTE COM LOGS DETALHADOS ===")

# 1. Login
print("1. Fazendo login...")
login_response = session.post("http://127.0.0.1:5000/admin/login", data={
    'username': 'admin',
    'password': 'senha123'
})
print(f"Login: {login_response.status_code}")

# 2. Aguardar um pouco
time.sleep(1)

# 3. Fazer requisição que deve gerar logs
print("2. Fazendo requisição para a API...")
print("Aguarde e veja os logs no servidor...")

response = session.post("http://127.0.0.1:5000/admin/adicionar-presente-por-link", 
                       json={"link": "https://www.americanas.com.br/produto/teste"})

print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('content-type')}")

if response.text.startswith('<!DOCTYPE html>'):
    print("❌ Retornou HTML - possível erro interno")
    # Procurar por indicadores de erro no HTML
    if "Internal Server Error" in response.text:
        print("💥 ERRO 500 - Internal Server Error")
    elif "404" in response.text:
        print("🔍 ERRO 404 - Rota não encontrada")
    elif "login" in response.text.lower():
        print("🔐 Possível problema de autenticação")
else:
    try:
        json_data = response.json()
        print(f"✅ JSON válido: {json_data}")
    except:
        print(f"📝 Resposta de texto: {response.text[:200]}")

print("=== VERIFIQUE OS LOGS DO SERVIDOR ===")
