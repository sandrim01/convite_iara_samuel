import requests
import time

# Teste simples para verificar se o servidor está respondendo
url = "http://127.0.0.1:5000/admin/presentes"

try:
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
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
        
except Exception as e:
    print(f"Erro ao acessar página: {e}")
