import requests

try:
    # Tentar a rota nova primeiro
    response = requests.get("http://127.0.0.1:5000/local-teste", timeout=5)
    print(f"Local-teste: {response.status_code}")
    
    response = requests.get("http://127.0.0.1:5000/local", timeout=5)
    print(f"Local: {response.status_code}")
    
    # Test POST to confirmation
    data = {'nome': 'Teste Novo', 'telefone': '123', 'email': 'test@novo.com', 'acompanhantes': '0'}
    response = requests.post("http://127.0.0.1:5000/processar-confirmacao", data=data, timeout=5, allow_redirects=False)
    print(f"Confirmação: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirecionado para: {response.headers.get('Location')}")
    
except Exception as e:
    print(f"Erro: {e}")
