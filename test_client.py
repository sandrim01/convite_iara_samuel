from app import create_app

app = create_app()

with app.test_client() as client:
    print("🔍 Testando rotas com Flask test client...")
    
    # Testar página principal
    response = client.get('/')
    print(f"/ -> Status: {response.status_code}")
    
    # Testar local
    response = client.get('/local')
    print(f"/local -> Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Data: {response.data.decode('utf-8')[:200]}")
    
    # Testar presentes
    response = client.get('/presentes')
    print(f"/presentes -> Status: {response.status_code}")
    
    # Testar confirmação
    data = {
        'nome': 'Teste Cliente',
        'telefone': '(11) 99999-9999',
        'email': 'teste@cliente.com',
        'acompanhantes': '1',
        'observacoes': 'Teste com Flask client'
    }
    response = client.post('/processar-confirmacao', data=data, follow_redirects=False)
    print(f"/processar-confirmacao -> Status: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirecionado para: {response.location}")
    elif response.status_code != 200:
        print(f"Data: {response.data.decode('utf-8')[:200]}")
