import requests
import time

# Teste com login
session = requests.Session()

# Primeiro, fazer login
login_url = "http://127.0.0.1:5000/admin/login"
login_data = {
    'username': 'master',
    'password': 'master123'
}

try:
    # Fazer login
    login_response = session.post(login_url, data=login_data)
    print(f"Login Status Code: {login_response.status_code}")
    
    # Agora acessar a página de presentes
    presentes_url = "http://127.0.0.1:5000/admin/presentes"
    response = session.get(presentes_url)
    print(f"Presentes Status Code: {response.status_code}")
    print(f"Content Length: {len(response.text)}")
    
    # Verificar se o JavaScript está presente
    if "abrirModalAdicionarPresente" in response.text:
        print("✅ Função JavaScript encontrada no HTML")
    else:
        print("❌ Função JavaScript NÃO encontrada no HTML")
        
    # Verificar se o modal está presente
    if "modalAdicionarPresente" in response.text:
        print("✅ Modal encontrado no HTML")
    else:
        print("❌ Modal NÃO encontrado no HTML")
        
    # Verificar se o botão está presente
    if 'onclick="abrirModalAdicionarPresente()"' in response.text:
        print("✅ Botão com onclick encontrado no HTML")
    else:
        print("❌ Botão com onclick NÃO encontrado no HTML")
        
    # Salvar HTML para debug
    with open('debug_presentes.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("HTML salvo em debug_presentes.html para análise")
        
except Exception as e:
    print(f"Erro: {e}")
