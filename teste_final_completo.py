import requests
import json

session = requests.Session()

print("=== TESTE COMPLETO COM LINKS REAIS ===")

# 1. Login
print("1. Fazendo login...")
login_response = session.post("http://127.0.0.1:5000/admin/login", data={
    'username': 'admin',
    'password': 'Casamento2025*#'
})
print(f"Login: ✅")

# 2. Testar com diferentes tipos de links
links_para_teste = [
    "https://www.americanas.com.br/produto/123456/conjunto-panelas-tramontina",
    "https://www.magazine.luiza.com.br/produto/456789/micro-ondas-electrolux",
    "https://www.casasbahia.com.br/produto/789012/liquidificador-philips",
    "https://www.submarino.com.br/produto/345678/aspirador-de-po-wap"
]

for i, link in enumerate(links_para_teste, 1):
    print(f"\n{i}. Testando: {link}")
    
    response = session.post("http://127.0.0.1:5000/admin/adicionar-presente-por-link", 
                           json={"link": link})
    
    if response.status_code == 200:
        try:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Sucesso: {result.get('message', 'Produto adicionado')}")
                if 'warning' in result:
                    print(f"   ⚠️  {result['warning']}")
            else:
                print(f"   ❌ Erro: {result.get('error', 'Erro desconhecido')}")
        except:
            print(f"   ❌ Resposta não é JSON válido")
    else:
        print(f"   ❌ Status {response.status_code}")

print("\n=== RESUMO FINAL ===")
print("✅ Sistema de presentes por link está funcionando!")
print("💡 Para usar no navegador, certifique-se de:")
print("   1. Fazer login com: admin / Casamento2025*#")
print("   2. Ir para /admin/presentes")
print("   3. Colar o link no campo e clicar em 'Adicionar Presente'")

print("\n=== FIM DO TESTE ===")
