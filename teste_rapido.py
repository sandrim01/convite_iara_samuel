import requests

# Teste simples do modal
data = {
    'nome': 'Teste Modal',
    'telefone': '11999999999', 
    'email': 'teste@modal.com',
    'acompanhantes': '2',
    'observacoes': 'Teste funcionamento'
}

try:
    r = requests.post('http://localhost:5000/processar-confirmacao', 
                     data=data, allow_redirects=False)
    print(f'Status: {r.status_code}')
    print(f'Redirect: {r.headers.get("Location", "Nenhum")}')
    
    if r.status_code == 302 and 'presentes' in r.headers.get("Location", ""):
        print('🎉 MODAL FUNCIONANDO!')
    else:
        print('❌ Problema no modal')
        
except Exception as e:
    print(f'Erro: {e}')
