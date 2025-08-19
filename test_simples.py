import requests

try:
    response = requests.get("http://127.0.0.1:5000", timeout=5)
    print(f"Index: {response.status_code}")
    
    response = requests.get("http://127.0.0.1:5000/local", timeout=5)
    print(f"Local: {response.status_code}")
    
    response = requests.get("http://127.0.0.1:5000/presentes", timeout=5)
    print(f"Presentes: {response.status_code}")
    
    # Test POST to confirmation
    data = {'nome': 'Teste', 'telefone': '123', 'email': 'test@test.com', 'acompanhantes': '0'}
    response = requests.post("http://127.0.0.1:5000/processar-confirmacao", data=data, timeout=5, allow_redirects=False)
    print(f"Confirmação: {response.status_code}")
    
except Exception as e:
    print(f"Erro: {e}")
